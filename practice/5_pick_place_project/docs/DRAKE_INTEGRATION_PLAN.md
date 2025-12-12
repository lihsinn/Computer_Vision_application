# Drake 機械手臂整合計畫

## 📋 概述

目前的 AOI 系統使用 **Three.js + React Three Fiber** 來渲染機械手臂，並使用簡單的 IK (Inverse Kinematics) 計算。

Drake 是 MIT 開發的機器人工具箱，提供：
- ✅ 精確的運動學和動力學計算
- ✅ 軌跡優化和碰撞檢測
- ✅ MPC (Model Predictive Control)
- ✅ 真實的物理模擬

---

## 🏗️ 系統架構

### 當前架構
```
前端 (React + Three.js)
├── RoboticArm.tsx         # 視覺化
├── simulatorStore.ts      # 狀態管理
└── 簡單 IK 計算            # TypeScript 實現
```

### 建議的新架構

```
┌─────────────────────────────────────────────────────────┐
│                    前端 (React)                          │
│  ┌───────────────┐         ┌─────────────────────┐     │
│  │  Three.js     │  ◄───── │  WebSocket Client   │     │
│  │  渲染器       │         │  (實時更新)          │     │
│  └───────────────┘         └─────────────────────┘     │
└─────────────────────────────────────────────────────────┘
                              ▲
                              │ WebSocket / REST API
                              ▼
┌─────────────────────────────────────────────────────────┐
│                 後端 (Python + Flask)                    │
│  ┌───────────────────────────────────────────────────┐ │
│  │              Drake Robotics Engine                 │ │
│  │  ┌──────────────┐  ┌──────────────┐              │ │
│  │  │  運動學計算  │  │  軌跡規劃    │              │ │
│  │  └──────────────┘  └──────────────┘              │ │
│  │  ┌──────────────┐  ┌──────────────┐              │ │
│  │  │  碰撞檢測    │  │  動力學模擬  │              │ │
│  │  └──────────────┘  └──────────────┘              │ │
│  └───────────────────────────────────────────────────┘ │
│  ┌───────────────────────────────────────────────────┐ │
│  │         現有 AOI 檢測模組                          │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 實作步驟

### Phase 1: Drake 後端設置

#### 1.1 安裝 Drake
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install drake

# 或使用 pip (推薦)
pip install drake
```

#### 1.2 建立 Drake 服務
創建 `aoi-system/backend/app/services/drake_service.py`

```python
from pydrake.all import (
    MultibodyPlant,
    SceneGraph,
    Parser,
    InverseKinematics,
    Solve
)
import numpy as np

class DrakeArmController:
    """Drake 機械手臂控制器"""

    def __init__(self, urdf_path):
        """
        初始化 Drake 機械手臂

        Args:
            urdf_path: 機械手臂的 URDF 檔案路徑
        """
        # 建立 MultibodyPlant
        self.plant = MultibodyPlant(time_step=0.001)
        self.scene_graph = SceneGraph()

        # 載入機械手臂模型
        parser = Parser(self.plant, self.scene_graph)
        self.model_instance = parser.AddModelFromFile(urdf_path)

        # 完成建構
        self.plant.Finalize()

        # 獲取機械手臂資訊
        self.num_joints = self.plant.num_positions()

    def solve_ik(self, target_position, target_orientation=None):
        """
        求解逆運動學

        Args:
            target_position: 目標位置 [x, y, z]
            target_orientation: 目標姿態（可選）

        Returns:
            joint_angles: 關節角度解
            success: 是否成功求解
        """
        ik = InverseKinematics(self.plant)

        # 設定末端效應器約束
        end_effector = self.plant.GetBodyByName("end_effector")

        # 位置約束
        ik.AddPositionConstraint(
            end_effector,
            [0, 0, 0],  # 末端效應器上的點
            self.plant.world_frame(),
            target_position,
            target_position
        )

        # 如果有姿態約束
        if target_orientation is not None:
            ik.AddOrientationConstraint(
                end_effector,
                self.plant.world_frame(),
                target_orientation,
                tolerance=0.01
            )

        # 求解
        result = Solve(ik.prog())

        if result.is_success():
            joint_angles = result.GetSolution(ik.q())
            return joint_angles.tolist(), True
        else:
            return None, False

    def compute_forward_kinematics(self, joint_angles):
        """
        正向運動學：計算末端位置

        Args:
            joint_angles: 關節角度

        Returns:
            position: 末端位置 [x, y, z]
            orientation: 末端姿態（四元數）
        """
        context = self.plant.CreateDefaultContext()
        self.plant.SetPositions(context, joint_angles)

        end_effector = self.plant.GetBodyByName("end_effector")
        transform = self.plant.CalcRelativeTransform(
            context,
            self.plant.world_frame(),
            end_effector.body_frame()
        )

        position = transform.translation()
        orientation = transform.rotation().ToQuaternion()

        return position.tolist(), orientation.wxyz().tolist()

    def plan_trajectory(self, start_angles, end_angles, duration=2.0):
        """
        規劃平滑軌跡

        Args:
            start_angles: 起始關節角度
            end_angles: 目標關節角度
            duration: 運動時間（秒）

        Returns:
            trajectory: 軌跡點列表
        """
        # 使用三次多項式插值
        num_points = int(duration * 50)  # 50 Hz
        t = np.linspace(0, duration, num_points)

        trajectory = []
        for i in range(num_points):
            s = t[i] / duration
            # 三次插值: s(t) = 3t^2 - 2t^3
            s_smooth = 3 * s**2 - 2 * s**3

            angles = (np.array(start_angles) +
                     s_smooth * (np.array(end_angles) - np.array(start_angles)))

            trajectory.append({
                "time": t[i],
                "joint_angles": angles.tolist()
            })

        return trajectory
```

#### 1.3 建立 API 端點
創建 `aoi-system/backend/app/routes/drake_robot.py`

```python
from flask import Blueprint, request, jsonify
from app.services.drake_service import DrakeArmController

drake_bp = Blueprint('drake', __name__)

# 初始化 Drake 控制器
# 注意：需要先準備 URDF 檔案
drake_controller = DrakeArmController("models/ur5.urdf")

@drake_bp.route('/api/drake/ik', methods=['POST'])
def solve_inverse_kinematics():
    """求解逆運動學"""
    data = request.json
    target_pos = data['target_position']  # [x, y, z]
    target_ori = data.get('target_orientation')  # optional

    joint_angles, success = drake_controller.solve_ik(
        target_pos,
        target_ori
    )

    return jsonify({
        "success": success,
        "joint_angles": joint_angles
    })

@drake_bp.route('/api/drake/fk', methods=['POST'])
def forward_kinematics():
    """正向運動學"""
    data = request.json
    joint_angles = data['joint_angles']

    position, orientation = drake_controller.compute_forward_kinematics(
        joint_angles
    )

    return jsonify({
        "position": position,
        "orientation": orientation
    })

@drake_bp.route('/api/drake/plan_trajectory', methods=['POST'])
def plan_trajectory():
    """規劃軌跡"""
    data = request.json
    start = data['start_angles']
    end = data['end_angles']
    duration = data.get('duration', 2.0)

    trajectory = drake_controller.plan_trajectory(start, end, duration)

    return jsonify({
        "trajectory": trajectory
    })
```

---

### Phase 2: 前端整合

#### 2.1 建立 Drake API Client
創建 `aoi-system/frontend/src/services/drakeApi.ts`

```typescript
import axios from 'axios';

const DRAKE_API_BASE = 'http://localhost:5000/api/drake';

export interface JointAngles {
  joint1: number;
  joint2: number;
  joint3: number;
  joint4: number;
  joint5: number;
  joint6: number;
}

export interface Position3D {
  x: number;
  y: number;
  z: number;
}

export interface Trajectory {
  time: number;
  joint_angles: number[];
}

export const drakeApi = {
  /**
   * 求解逆運動學
   */
  async solveIK(
    targetPosition: Position3D,
    targetOrientation?: number[]
  ): Promise<number[]> {
    const response = await axios.post(`${DRAKE_API_BASE}/ik`, {
      target_position: [targetPosition.x, targetPosition.y, targetPosition.z],
      target_orientation: targetOrientation,
    });

    if (response.data.success) {
      return response.data.joint_angles;
    } else {
      throw new Error('IK solution not found');
    }
  },

  /**
   * 正向運動學
   */
  async computeFK(jointAngles: number[]): Promise<{
    position: Position3D;
    orientation: number[];
  }> {
    const response = await axios.post(`${DRAKE_API_BASE}/fk`, {
      joint_angles: jointAngles,
    });

    const pos = response.data.position;
    return {
      position: { x: pos[0], y: pos[1], z: pos[2] },
      orientation: response.data.orientation,
    };
  },

  /**
   * 規劃軌跡
   */
  async planTrajectory(
    startAngles: number[],
    endAngles: number[],
    duration: number = 2.0
  ): Promise<Trajectory[]> {
    const response = await axios.post(`${DRAKE_API_BASE}/plan_trajectory`, {
      start_angles: startAngles,
      end_angles: endAngles,
      duration,
    });

    return response.data.trajectory;
  },
};
```

#### 2.2 更新 RoboticArm 組件
修改 `aoi-system/frontend/src/components/3d/RoboticArm.tsx`

```typescript
import { useEffect, useState } from 'react';
import { drakeApi } from '../../services/drakeApi';

const RoboticArm: React.FC = () => {
  const [jointAngles, setJointAngles] = useState<number[]>([0, 0, 0, 0, 0, 0]);
  const armTarget = useSimulatorStore((state) => state.armTarget);

  // 使用 Drake 計算 IK
  useEffect(() => {
    if (armTarget) {
      drakeApi
        .solveIK({
          x: armTarget[0],
          y: armTarget[1],
          z: armTarget[2],
        })
        .then((angles) => {
          setJointAngles(angles);
          // 更新 Three.js 視覺化
          armSpringApi.start({
            baseRotation: angles[0],
            shoulderRotation: angles[1],
            elbowRotation: angles[2],
            wristRotation: angles[3],
          });
        })
        .catch((error) => {
          console.error('IK failed:', error);
        });
    }
  }, [armTarget]);

  // ... 其餘視覺化代碼保持不變
};
```

---

### Phase 3: URDF 模型準備

#### 3.1 建立機械手臂 URDF
創建 `aoi-system/backend/models/ur5.urdf`

你需要為你的機械手臂創建 URDF（Unified Robot Description Format）檔案。

**選項 1: 使用現有模型**
- UR5: https://github.com/ros-industrial/universal_robot
- 其他機械手臂: 搜尋 "[robot_name] urdf github"

**選項 2: 自己建立**
```xml
<?xml version="1.0"?>
<robot name="my_robot_arm">
  <!-- 定義連桿和關節 -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder length="0.3" radius="0.5"/>
      </geometry>
    </visual>
  </link>

  <link name="shoulder_link">
    <!-- ... -->
  </link>

  <joint name="base_to_shoulder" type="revolute">
    <parent link="base_link"/>
    <child link="shoulder_link"/>
    <origin xyz="0 0 0.35"/>
    <axis xyz="0 0 1"/>
    <limit lower="-3.14" upper="3.14" effort="100" velocity="1.0"/>
  </joint>

  <!-- 繼續定義其他連桿和關節 -->
</robot>
```

---

## 📊 整合檢測角度

將物件旋轉檢測整合到機械手臂控制：

```python
# aoi-system/backend/app/services/pick_place_service.py
from app.services.drake_service import DrakeArmController
from app.services.aoi_service import detect_object_rotation

class PickPlaceService:
    def __init__(self):
        self.drake = DrakeArmController("models/ur5.urdf")

    def pick_object(self, image, object_bbox):
        """
        抓取物件的完整流程
        """
        # 1. 檢測物件旋轉角度
        rotation_angle = detect_object_rotation(image, object_bbox)

        # 2. 計算抓取位置（像素 -> 機器人座標）
        center_x = (object_bbox['x1'] + object_bbox['x2']) / 2
        center_y = (object_bbox['y1'] + object_bbox['y2']) / 2

        # 座標轉換（需要相機標定）
        robot_x = self.pixel_to_robot_x(center_x)
        robot_y = self.pixel_to_robot_y(center_y)
        robot_z = 0.0  # 抓取高度

        # 3. 計算末端姿態（考慮旋轉角度）
        target_orientation = self.compute_gripper_orientation(rotation_angle)

        # 4. 使用 Drake 求解 IK
        joint_angles, success = self.drake.solve_ik(
            [robot_x, robot_y, robot_z],
            target_orientation
        )

        if not success:
            return {"error": "IK solution not found"}

        # 5. 規劃軌跡
        current_angles = self.get_current_joint_angles()
        trajectory = self.drake.plan_trajectory(
            current_angles,
            joint_angles,
            duration=2.0
        )

        return {
            "success": True,
            "rotation_angle": rotation_angle,
            "joint_angles": joint_angles,
            "trajectory": trajectory
        }
```

---

## ⚠️ 注意事項

### 1. 效能考量
- Drake 計算可能較慢（尤其是複雜的 IK）
- 建議使用 WebSocket 進行即時通訊
- 考慮在後端快取計算結果

### 2. 相機標定
- 必須進行準確的相機標定
- 建立像素座標到機器人座標的映射
- 考慮鏡頭畸變矯正

### 3. 安全性
- 加入工作空間限制
- 碰撞檢測
- 速度和加速度限制

---

## 🎯 測試計畫

### 單元測試
```python
# tests/test_drake_service.py
def test_ik_solution():
    drake = DrakeArmController("models/ur5.urdf")
    target = [0.4, 0.2, 0.3]
    angles, success = drake.solve_ik(target)
    assert success
    assert len(angles) == 6

def test_fk_matches_ik():
    drake = DrakeArmController("models/ur5.urdf")
    target = [0.4, 0.2, 0.3]

    # IK
    angles, _ = drake.solve_ik(target)

    # FK
    position, _ = drake.compute_forward_kinematics(angles)

    # 驗證誤差 < 1mm
    error = np.linalg.norm(np.array(position) - np.array(target))
    assert error < 0.001
```

### 整合測試
1. 後端 API 測試
2. 前端顯示測試
3. 完整流程測試（檢測 → 規劃 → 執行）

---

## 📚 參考資源

- [Drake 官方文件](https://drake.mit.edu/)
- [Drake Python API](https://drake.mit.edu/pydrake/index.html)
- [URDF 教學](http://wiki.ros.org/urdf/Tutorials)
- [機械手臂運動學](https://robotacademy.net.au/)

---

## 🚀 下一步

1. ✅ 先完成旋轉角度檢測練習
2. ⬜ 安裝 Drake 並測試基本功能
3. ⬜ 準備機械手臂 URDF 模型
4. ⬜ 建立後端 Drake 服務
5. ⬜ 前端整合
6. ⬜ 整合檢測與控制
7. ⬜ 測試與優化
