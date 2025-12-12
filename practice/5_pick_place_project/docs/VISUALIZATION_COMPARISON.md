# 視覺化方案比較

## 🎨 Three.js vs Drake MeshCat

### 當前方案：Three.js + React Three Fiber

**優點：**
- ✅ 美觀的自定義 3D 渲染
- ✅ 完全控制視覺效果
- ✅ 與 React 無縫整合
- ✅ 豐富的動畫效果
- ✅ 快速渲染

**缺點：**
- ❌ 需要手動實現 IK
- ❌ 物理模擬不準確
- ❌ 沒有碰撞檢測
- ❌ 軌跡規劃需要自己實現

**適合場景：**
- 視覺展示為主
- 不需要精確物理模擬
- 重視美觀和流暢度

---

### 建議方案：Drake MeshCat

**優點：**
- ✅ 精確的運動學和動力學
- ✅ 內建碰撞檢測
- ✅ 專業的軌跡規劃
- ✅ 真實的物理模擬
- ✅ URDF 模型支援
- ✅ 可匯出真實機器人代碼

**缺點：**
- ❌ 視覺效果較簡單
- ❌ 自定義樣式困難
- ❌ 需要 Python 後端
- ❌ 學習曲線較陡

**適合場景：**
- 需要精確模擬
- 規劃真實機器人動作
- 研究和開發用途

---

## 🏗️ 混合方案（推薦）

**結合兩者優點：**

```
┌─────────────────────────────────────────────────┐
│            前端 (React)                          │
│  ┌──────────────┐      ┌──────────────────┐    │
│  │  Three.js    │      │  Drake MeshCat   │    │
│  │  美化展示    │      │  精確模擬        │    │
│  │  (主要視圖)  │      │  (可切換)        │    │
│  └──────────────┘      └──────────────────┘    │
│         ▲                      ▲                 │
│         │                      │                 │
│         └──────────┬───────────┘                 │
│                    │                             │
└────────────────────┼─────────────────────────────┘
                     │ WebSocket
                     ▼
┌─────────────────────────────────────────────────┐
│          後端 (Python + Flask)                   │
│  ┌───────────────────────────────────────────┐  │
│  │        Drake 運動規劃引擎                  │  │
│  │  - IK/FK 計算                              │  │
│  │  - 軌跡規劃                                │  │
│  │  - 碰撞檢測                                │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### 工作流程：

1. **Drake 後端**：
   - 進行精確的 IK/FK 計算
   - 規劃平滑軌跡
   - 檢測碰撞
   - 驗證動作可行性

2. **前端顯示**：
   - **主視圖**：Three.js 渲染（美觀流暢）
   - **驗證視圖**：Drake MeshCat（精確模擬）
   - 使用者可以切換視圖

3. **數據同步**：
   - 後端計算關節角度
   - WebSocket 即時傳送
   - 兩個視圖同步更新

---

## 📊 實作範例

### 1. 後端：Drake 計算 + MeshCat

```python
# backend/app/services/drake_hybrid_service.py

from pydrake.all import *
from flask_socketio import SocketIO

class DrakeHybridService:
    def __init__(self, socketio):
        self.socketio = socketio

        # Drake 模擬器（用於計算）
        self.setup_drake()

        # MeshCat（用於驗證視覺化）
        self.meshcat = StartMeshcat()

    def setup_drake(self):
        self.builder = DiagramBuilder()
        self.plant, self.scene_graph = \
            MultibodyPlant.AddMultibodyPlantSceneGraph(
                self.builder, time_step=0.001
            )

        parser = Parser(self.plant, self.scene_graph)
        parser.AddModelFromFile("models/ur5.urdf")
        self.plant.Finalize()

        # 添加 MeshCat 視覺化
        MeshcatVisualizer.AddToBuilder(
            self.builder,
            self.scene_graph,
            self.meshcat
        )

        self.diagram = self.builder.Build()
        self.simulator = Simulator(self.diagram)

    def plan_motion(self, start_pos, end_pos, rotation_angle):
        '''規劃動作並返回軌跡'''

        # 1. 計算起點和終點的關節角度
        q_start = self.solve_ik(start_pos, rotation_angle)
        q_end = self.solve_ik(end_pos, rotation_angle)

        if q_start is None or q_end is None:
            return None

        # 2. 使用 Drake 規劃平滑軌跡
        trajectory = self.plan_trajectory(q_start, q_end)

        # 3. 更新 MeshCat 視覺化
        self.update_meshcat_visualization(trajectory)

        # 4. 發送軌跡到前端
        self.socketio.emit('trajectory_update', {
            'trajectory': trajectory,
            'meshcat_url': self.meshcat.web_url()
        })

        return trajectory

    def solve_ik(self, position, rotation):
        '''求解 IK'''
        ik = InverseKinematics(self.plant)

        # 末端效應器
        ee_frame = self.plant.GetFrameByName("end_effector")

        # 位置約束
        ik.AddPositionConstraint(
            ee_frame,
            [0, 0, 0],
            self.plant.world_frame(),
            position,
            position
        )

        # 姿態約束（考慮旋轉角度）
        R = RotationMatrix.MakeZRotation(np.radians(rotation))
        ik.AddOrientationConstraint(
            ee_frame,
            R,
            self.plant.world_frame(),
            RotationMatrix(),
            0.01
        )

        result = Solve(ik.prog())

        if result.is_success():
            return result.GetSolution(ik.q())
        return None

    def plan_trajectory(self, q_start, q_end, duration=2.0):
        '''規劃軌跡'''
        # 使用三次多項式插值
        num_points = int(duration * 50)  # 50 Hz
        t = np.linspace(0, duration, num_points)

        trajectory = []
        for i in range(num_points):
            s = t[i] / duration
            s_smooth = 3 * s**2 - 2 * s**3  # 平滑插值

            q = q_start + s_smooth * (q_end - q_start)

            # 計算末端位置（用於前端顯示）
            pos, rot = self.compute_forward_kinematics(q)

            trajectory.append({
                'time': t[i],
                'joint_angles': q.tolist(),
                'end_effector_pos': pos,
                'end_effector_rot': rot
            })

        return trajectory

    def compute_forward_kinematics(self, q):
        '''正向運動學'''
        context = self.plant.CreateDefaultContext()
        self.plant.SetPositions(context, q)

        ee_frame = self.plant.GetFrameByName("end_effector")
        transform = self.plant.CalcRelativeTransform(
            context,
            self.plant.world_frame(),
            ee_frame
        )

        return (
            transform.translation().tolist(),
            transform.rotation().ToQuaternion().wxyz().tolist()
        )

    def update_meshcat_visualization(self, trajectory):
        '''更新 MeshCat 視覺化'''
        context = self.simulator.get_mutable_context()

        for point in trajectory:
            q = np.array(point['joint_angles'])
            self.plant.SetPositions(
                self.plant.GetMyContextFromRoot(context),
                q
            )
            self.diagram.ForcedPublish(context)
```

### 2. 前端：雙視圖顯示

```typescript
// frontend/src/components/HybridViewer.tsx

import React, { useState, useEffect } from 'react';
import {
  Box,
  Tabs,
  Tab,
  Paper,
  Switch,
  FormControlLabel
} from '@mui/material';
import Scene3D from './3d/Scene3D';  // Three.js 視圖
import io from 'socket.io-client';

interface TrajectoryPoint {
  time: number;
  joint_angles: number[];
  end_effector_pos: number[];
  end_effector_rot: number[];
}

const HybridViewer: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [meshcatUrl, setMeshcatUrl] = useState<string>('');
  const [trajectory, setTrajectory] = useState<TrajectoryPoint[]>([]);
  const [currentFrame, setCurrentFrame] = useState(0);
  const [syncViews, setSyncViews] = useState(true);

  useEffect(() => {
    // 獲取 MeshCat URL
    fetch('/api/meshcat_url')
      .then(res => res.json())
      .then(data => setMeshcatUrl(data.url));

    // 連接 WebSocket
    const socket = io('http://localhost:5000');

    socket.on('trajectory_update', (data) => {
      console.log('Trajectory received:', data);
      setTrajectory(data.trajectory);
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  // 動畫播放
  useEffect(() => {
    if (trajectory.length === 0) return;

    const interval = setInterval(() => {
      setCurrentFrame(prev => {
        const next = (prev + 1) % trajectory.length;
        return next;
      });
    }, 1000 / 50);  // 50 Hz

    return () => clearInterval(interval);
  }, [trajectory]);

  return (
    <Box>
      {/* 視圖切換標籤 */}
      <Paper sx={{ mb: 2 }}>
        <Tabs value={activeTab} onChange={(e, v) => setActiveTab(v)}>
          <Tab label="🎨 Three.js (美化)" />
          <Tab label="🔬 Drake MeshCat (精確)" />
          <Tab label="📊 分屏比較" />
        </Tabs>

        <Box sx={{ p: 2 }}>
          <FormControlLabel
            control={
              <Switch
                checked={syncViews}
                onChange={(e) => setSyncViews(e.target.checked)}
              />
            }
            label="同步兩個視圖"
          />
        </Box>
      </Paper>

      {/* Three.js 視圖 */}
      {(activeTab === 0 || activeTab === 2) && (
        <Box sx={{
          width: activeTab === 2 ? '50%' : '100%',
          display: 'inline-block'
        }}>
          <Scene3D
            jointAngles={
              trajectory[currentFrame]?.joint_angles || []
            }
          />
        </Box>
      )}

      {/* Drake MeshCat 視圖 */}
      {(activeTab === 1 || activeTab === 2) && (
        <Box sx={{
          width: activeTab === 2 ? '50%' : '100%',
          display: 'inline-block'
        }}>
          {meshcatUrl && (
            <iframe
              src={meshcatUrl}
              style={{
                width: '100%',
                height: '600px',
                border: 'none'
              }}
              title="Drake MeshCat"
            />
          )}
        </Box>
      )}
    </Box>
  );
};

export default HybridViewer;
```

### 3. API 路由

```python
# backend/app/routes/hybrid_sim.py

from flask import Blueprint, jsonify, request
from app.services.drake_hybrid_service import drake_service

hybrid_bp = Blueprint('hybrid', __name__)

@hybrid_bp.route('/api/meshcat_url')
def get_meshcat_url():
    '''獲取 MeshCat URL'''
    return jsonify({
        'url': drake_service.meshcat.web_url()
    })

@hybrid_bp.route('/api/plan_pick', methods=['POST'])
def plan_pick_motion():
    '''規劃抓取動作'''
    data = request.json

    # 物件位置和旋轉角度（來自視覺檢測）
    object_pos = data['object_position']  # [x, y, z]
    rotation = data['rotation_angle']     # degrees

    # 當前位置
    current_pos = data['current_position']

    # 使用 Drake 規劃動作
    trajectory = drake_service.plan_motion(
        start_pos=current_pos,
        end_pos=object_pos,
        rotation_angle=rotation
    )

    if trajectory:
        return jsonify({
            'success': True,
            'trajectory': trajectory
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Motion planning failed'
        }), 400
```

---

## 🎯 推薦實作步驟

### Phase 1: 保留 Three.js，加入 Drake 後端

1. ✅ 安裝 Drake
2. ✅ 創建 Drake 服務類別
3. ✅ 建立 API 端點
4. ✅ 前端透過 API 獲取計算結果
5. ✅ Three.js 使用 Drake 計算的角度

**優點**：漸進式整合，風險低

### Phase 2: 加入 Drake MeshCat 視圖

1. ✅ 啟動 MeshCat 服務
2. ✅ 前端添加 iframe 顯示 MeshCat
3. ✅ 實作視圖切換功能
4. ✅ 同步兩個視圖的狀態

**優點**：可以驗證精確度

### Phase 3: 完整整合

1. ✅ 整合物件檢測
2. ✅ 自動規劃抓取動作
3. ✅ 碰撞檢測
4. ✅ 多物件處理

---

## 💡 最終建議

**對於你的 AOI 系統，建議使用混合方案：**

1. **開發/測試階段**：
   - 主要使用 Drake MeshCat
   - 確保動作精確無誤
   - 驗證碰撞檢測

2. **展示/生產階段**：
   - 主要使用 Three.js
   - 美觀流暢的視覺效果
   - 必要時切換到 Drake 驗證

3. **實際部署到機器人**：
   - 使用 Drake 生成的軌跡
   - 直接轉換為機器人指令
   - 保證精確性和安全性

---

## 📚 下一步

1. 試運行 `02_drake_visualization.py`
2. 熟悉 Drake 的 IK 和軌跡規劃
3. 整合旋轉角度檢測
4. 建立混合視圖系統
