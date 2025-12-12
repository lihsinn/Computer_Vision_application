"""
Drake 機械手臂視覺化示範
Drake Robotic Arm Visualization with MeshCat

展示如何使用 Drake 的 MeshCat 進行 3D 視覺化
"""

import numpy as np
from pydrake.all import (
    DiagramBuilder,
    MultibodyPlant,
    SceneGraph,
    Parser,
    Simulator,
    MeshcatVisualizer,
    StartMeshcat,
    RigidTransform,
    RotationMatrix,
    InverseKinematics,
    Solve,
)


class DrakeArmSimulator:
    """Drake 機械手臂模擬器"""

    def __init__(self, urdf_path=None):
        """
        初始化 Drake 模擬器

        Args:
            urdf_path: URDF 檔案路徑（如果為 None，使用簡單模型）
        """
        self.builder = DiagramBuilder()
        self.plant = None
        self.scene_graph = None
        self.meshcat = None
        self.visualizer = None
        self.urdf_path = urdf_path

        self._setup_plant()
        self._setup_visualization()

    def _setup_plant(self):
        """設置 MultibodyPlant"""
        # 創建 plant 和 scene_graph
        self.plant, self.scene_graph = MultibodyPlant.AddMultibodyPlantSceneGraph(
            self.builder, time_step=0.001
        )

        if self.urdf_path:
            # 載入 URDF 模型
            parser = Parser(self.plant, self.scene_graph)
            self.model_instance = parser.AddModelFromFile(self.urdf_path)
        else:
            # 創建簡單的 3-link 手臂示範
            self._create_simple_arm()

        # 完成 plant 建構
        self.plant.Finalize()

    def _create_simple_arm(self):
        """創建簡單的 3 連桿手臂（示範用）"""
        # 這裡會創建一個簡化的手臂模型
        # 實際使用時應該載入 URDF

        # 基座
        base_body = self.plant.AddRigidBody(
            "base",
            self.plant.world_body(),
            RigidTransform()
        )

        # 後續會在 URDF 示範中完整實現
        pass

    def _setup_visualization(self):
        """設置 MeshCat 視覺化"""
        # 啟動 MeshCat 服務器
        self.meshcat = StartMeshcat()

        # 添加 MeshCat 視覺化器到系統
        self.visualizer = MeshcatVisualizer.AddToBuilder(
            self.builder,
            self.scene_graph,
            self.meshcat
        )

        # 設置相機視角
        self.meshcat.SetCameraPose([2, 2, 2], [0, 0, 0])

    def solve_ik(self, target_position, target_orientation=None):
        """
        求解逆運動學

        Args:
            target_position: [x, y, z] 目標位置
            target_orientation: 目標姿態（可選）

        Returns:
            joint_angles: 關節角度
            success: 是否成功
        """
        context = self.plant.CreateDefaultContext()
        ik = InverseKinematics(self.plant, context)

        # 獲取末端效應器
        end_effector_frame = self.plant.GetFrameByName("end_effector")

        # 位置約束
        p_target = np.array(target_position)
        ik.AddPositionConstraint(
            end_effector_frame,
            [0, 0, 0],
            self.plant.world_frame(),
            p_target - 0.01,  # 允許小誤差
            p_target + 0.01
        )

        # 如果有姿態約束
        if target_orientation is not None:
            R_target = RotationMatrix(target_orientation)
            ik.AddOrientationConstraint(
                end_effector_frame,
                R_target,
                self.plant.world_frame(),
                RotationMatrix(),
                0.01
            )

        # 求解
        result = Solve(ik.prog())

        if result.is_success():
            q = result.GetSolution(ik.q())
            return q, True
        else:
            return None, False

    def run_simulation(self, duration=5.0):
        """
        執行模擬

        Args:
            duration: 模擬時間（秒）
        """
        # 建構完整系統
        diagram = self.builder.Build()

        # 創建模擬器
        simulator = Simulator(diagram)
        simulator.set_target_realtime_rate(1.0)

        # 執行模擬
        print(f"開始模擬 {duration} 秒...")
        print(f"MeshCat 視覺化：在瀏覽器中打開 {self.meshcat.web_url()}")

        simulator.AdvanceTo(duration)

        print("模擬完成！")

    def animate_pick_and_place(self):
        """動畫示範：抓取和放置"""
        print("=" * 60)
        print("Drake 抓取與放置動畫示範")
        print("=" * 60)

        # 定義關鍵點
        waypoints = [
            # 初始位置
            {"position": [0.3, 0, 0.5], "duration": 0},

            # 移動到物件上方
            {"position": [0.4, 0.2, 0.3], "duration": 2.0},

            # 下降抓取
            {"position": [0.4, 0.2, 0.1], "duration": 1.0},

            # 提升
            {"position": [0.4, 0.2, 0.3], "duration": 1.0},

            # 移動到放置位置
            {"position": [0.3, -0.3, 0.3], "duration": 2.0},

            # 下降放置
            {"position": [0.3, -0.3, 0.1], "duration": 1.0},

            # 回到初始位置
            {"position": [0.3, 0, 0.5], "duration": 2.0},
        ]

        # 建構系統
        diagram = self.builder.Build()
        simulator = Simulator(diagram)
        context = simulator.get_mutable_context()

        print(f"\n🌐 在瀏覽器中打開：{self.meshcat.web_url()}")
        print("\n執行抓取放置動畫...")

        total_time = 0
        for i, waypoint in enumerate(waypoints):
            print(f"\n階段 {i+1}: 移動到 {waypoint['position']}")

            # 求解 IK
            q, success = self.solve_ik(waypoint['position'])

            if success:
                # 設置關節角度
                self.plant.SetPositions(
                    self.plant.GetMyContextFromRoot(context),
                    q
                )

                # 更新視覺化
                diagram.ForcedPublish(context)

                # 等待
                if waypoint['duration'] > 0:
                    simulator.AdvanceTo(total_time + waypoint['duration'])
                    total_time += waypoint['duration']
            else:
                print(f"  ❌ IK 求解失敗！")

        print("\n✅ 動畫完成！")
        input("按 Enter 關閉...")


# ============================================
# 創建簡單的 URDF 範例
# ============================================

def create_simple_arm_urdf():
    """創建一個簡單的 3-link 機械手臂 URDF"""

    urdf_content = """<?xml version="1.0"?>
<robot name="simple_arm">

  <!-- 基座 -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder length="0.1" radius="0.1"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 1"/>
      </material>
    </visual>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.001"/>
    </inertial>
  </link>

  <!-- 連桿 1 -->
  <link name="link1">
    <visual>
      <origin xyz="0 0 0.15"/>
      <geometry>
        <cylinder length="0.3" radius="0.05"/>
      </geometry>
      <material name="blue">
        <color rgba="0.2 0.4 0.8 1"/>
      </material>
    </visual>
    <inertial>
      <origin xyz="0 0 0.15"/>
      <mass value="0.5"/>
      <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.0001"/>
    </inertial>
  </link>

  <!-- 關節 1: 基座到連桿1 -->
  <joint name="joint1" type="revolute">
    <parent link="base_link"/>
    <child link="link1"/>
    <origin xyz="0 0 0.05"/>
    <axis xyz="0 0 1"/>
    <limit lower="-3.14" upper="3.14" effort="100" velocity="1.0"/>
  </joint>

  <!-- 連桿 2 -->
  <link name="link2">
    <visual>
      <origin xyz="0 0 0.15"/>
      <geometry>
        <cylinder length="0.3" radius="0.04"/>
      </geometry>
      <material name="green">
        <color rgba="0.2 0.8 0.4 1"/>
      </material>
    </visual>
    <inertial>
      <origin xyz="0 0 0.15"/>
      <mass value="0.3"/>
      <inertia ixx="0.001" ixy="0" ixz="0" iyy="0.001" iyz="0" izz="0.0001"/>
    </inertial>
  </link>

  <!-- 關節 2: 連桿1到連桿2 -->
  <joint name="joint2" type="revolute">
    <parent link="link1"/>
    <child link="link2"/>
    <origin xyz="0 0 0.3"/>
    <axis xyz="1 0 0"/>
    <limit lower="-2.0" upper="2.0" effort="50" velocity="1.0"/>
  </joint>

  <!-- 連桿 3（末端效應器） -->
  <link name="link3">
    <visual>
      <origin xyz="0 0 0.1"/>
      <geometry>
        <cylinder length="0.2" radius="0.03"/>
      </geometry>
      <material name="red">
        <color rgba="0.8 0.2 0.2 1"/>
      </material>
    </visual>
    <inertial>
      <origin xyz="0 0 0.1"/>
      <mass value="0.2"/>
      <inertia ixx="0.0005" ixy="0" ixz="0" iyy="0.0005" iyz="0" izz="0.00001"/>
    </inertial>
  </link>

  <!-- 關節 3: 連桿2到連桿3 -->
  <joint name="joint3" type="revolute">
    <parent link="link2"/>
    <child link="link3"/>
    <origin xyz="0 0 0.3"/>
    <axis xyz="1 0 0"/>
    <limit lower="-2.0" upper="2.0" effort="30" velocity="1.0"/>
  </joint>

  <!-- 末端效應器座標系 -->
  <link name="end_effector">
    <visual>
      <geometry>
        <sphere radius="0.02"/>
      </geometry>
      <material name="yellow">
        <color rgba="1 1 0 1"/>
      </material>
    </visual>
    <inertial>
      <mass value="0.01"/>
      <inertia ixx="0.00001" ixy="0" ixz="0" iyy="0.00001" iyz="0" izz="0.00001"/>
    </inertial>
  </link>

  <joint name="ee_joint" type="fixed">
    <parent link="link3"/>
    <child link="end_effector"/>
    <origin xyz="0 0 0.2"/>
  </joint>

</robot>
"""

    # 儲存 URDF 檔案
    urdf_path = "practice/5_pick_place_project/simple_arm.urdf"
    with open(urdf_path, 'w', encoding='utf-8') as f:
        f.write(urdf_content)

    print(f"✅ URDF 檔案已創建：{urdf_path}")
    return urdf_path


# ============================================
# 整合到 AOI 系統的範例
# ============================================

def aoi_drake_integration_example():
    """
    展示如何整合 Drake 視覺化到 AOI 系統

    架構：
    1. Flask 後端運行 Drake 模擬
    2. WebSocket 傳送關節角度更新
    3. 前端透過 MeshCat iframe 顯示
    """

    example_code = """
# ===== 後端代碼 =====
# aoi-system/backend/app/services/drake_simulator.py

from pydrake.all import *
from flask_socketio import SocketIO, emit
import threading

class DrakeSimulatorService:
    def __init__(self, socketio):
        self.socketio = socketio
        self.meshcat = StartMeshcat()
        self.builder = DiagramBuilder()

        # 設置 plant
        self.plant, self.scene_graph = MultibodyPlant.AddMultibodyPlantSceneGraph(
            self.builder, time_step=0.001
        )

        # 載入模型
        parser = Parser(self.plant, self.scene_graph)
        parser.AddModelFromFile("models/ur5.urdf")
        self.plant.Finalize()

        # MeshCat 視覺化
        MeshcatVisualizer.AddToBuilder(
            self.builder,
            self.scene_graph,
            self.meshcat
        )

        self.diagram = self.builder.Build()
        self.simulator = Simulator(self.diagram)

    def get_meshcat_url(self):
        return self.meshcat.web_url()

    def move_to_target(self, target_position, rotation_angle):
        '''移動到目標位置並考慮旋轉角度'''

        # IK 求解
        ik = InverseKinematics(self.plant)
        # ... IK 設置 ...

        result = Solve(ik.prog())

        if result.is_success():
            q = result.GetSolution(ik.q())

            # 更新模擬
            context = self.simulator.get_mutable_context()
            self.plant.SetPositions(
                self.plant.GetMyContextFromRoot(context),
                q
            )

            # 發送更新到前端
            self.socketio.emit('robot_state_update', {
                'joint_angles': q.tolist(),
                'position': target_position,
                'rotation': rotation_angle
            })

            return True

        return False


# ===== Flask 路由 =====
# aoi-system/backend/app/__init__.py

from flask import Flask
from flask_socketio import SocketIO
from app.services.drake_simulator import DrakeSimulatorService

socketio = SocketIO()
drake_sim = None

def create_app():
    app = Flask(__name__)

    # 初始化 SocketIO
    socketio.init_app(app, cors_allowed_origins="*")

    # 初始化 Drake 模擬器
    global drake_sim
    drake_sim = DrakeSimulatorService(socketio)

    @app.route('/api/meshcat_url')
    def get_meshcat_url():
        return {'url': drake_sim.get_meshcat_url()}

    return app


# ===== 前端代碼 =====
// aoi-system/frontend/src/components/DrakeViewer.tsx

import React, { useEffect, useState } from 'react';
import { Box, CircularProgress } from '@mui/material';

const DrakeViewer: React.FC = () => {
  const [meshcatUrl, setMeshcatUrl] = useState<string | null>(null);

  useEffect(() => {
    // 獲取 MeshCat URL
    fetch('/api/meshcat_url')
      .then(res => res.json())
      .then(data => setMeshcatUrl(data.url));
  }, []);

  if (!meshcatUrl) {
    return (
      <Box display="flex" justifyContent="center" p={3}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ width: '100%', height: '600px' }}>
      <iframe
        src={meshcatUrl}
        style={{
          width: '100%',
          height: '100%',
          border: 'none',
          borderRadius: '8px'
        }}
        title="Drake MeshCat Viewer"
      />
    </Box>
  );
};

export default DrakeViewer;


// aoi-system/frontend/src/pages/DrakeSimulatorPage.tsx

import React, { useEffect } from 'react';
import { Container, Typography, Paper } from '@mui/material';
import DrakeViewer from '../components/DrakeViewer';
import io from 'socket.io-client';

const DrakeSimulatorPage: React.FC = () => {
  useEffect(() => {
    // 連接 WebSocket
    const socket = io('http://localhost:5000');

    socket.on('robot_state_update', (data) => {
      console.log('Robot state updated:', data);
      // 更新 UI 狀態顯示
    });

    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <Container maxWidth="xl" sx={{ py: 3 }}>
      <Typography variant="h4" gutterBottom>
        🤖 Drake 機械手臂模擬器
      </Typography>

      <Paper sx={{ p: 2, mt: 2 }}>
        <DrakeViewer />
      </Paper>

      {/* 控制面板、統計等 */}
    </Container>
  );
};

export default DrakeSimulatorPage;
"""

    print("=" * 60)
    print("Drake + AOI 系統整合範例")
    print("=" * 60)
    print(example_code)


# ============================================
# 主程式
# ============================================

def main():
    print("[Robot]  Drake 視覺化教學")
    print("=" * 60)

    print("\n步驟 1: 創建 URDF 模型")
    urdf_path = create_simple_arm_urdf()

    print("\n步驟 2: 啟動 Drake 模擬器")
    print("注意：這需要安裝 Drake")
    print("安裝指令：pip install drake")

    response = input("\n是否執行 Drake 模擬？(需要已安裝 Drake) [y/N]: ")

    if response.lower() == 'y':
        try:
            print("\n啟動 Drake 模擬器...")
            simulator = DrakeArmSimulator(urdf_path)
            simulator.animate_pick_and_place()

        except ImportError:
            print("\n[Error]  Drake 尚未安裝")
            print("請執行：pip install drake")
        except Exception as e:
            print(f"\n[Error]  錯誤：{e}")
            import traceback
            traceback.print_exc()
    else:
        print("\n跳過 Drake 模擬")

    print("\n步驟 3: 查看整合範例")
    aoi_drake_integration_example()

    print("\n" + "=" * 60)
    print("教學完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
