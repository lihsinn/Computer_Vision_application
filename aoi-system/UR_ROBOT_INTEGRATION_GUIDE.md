# UR 机器人 URDF 模型集成指南

## 📋 概述

本指南提供**三种方案**来集成真实的 Universal Robots (UR) 机器人模型到你的 AOI 系统中。

---

## 🎯 方案对比

| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| **方案 1: URDF 模型加载** | ✅ 真实模型外观<br>✅ 准确的几何结构 | ❌ 需要手动实现 IK<br>❌ 静态模型 | 可视化模拟 |
| **方案 2: ROS2 Bridge** | ✅ 真实运动学<br>✅ 可连接真实机器人<br>✅ ROS 生态系统 | ❌ 架构复杂<br>❌ 需要额外服务 | 真实机器人控制 |
| **方案 3: react-three/urdf** | ✅ React 原生集成<br>✅ 简单易用 | ❌ 功能有限 | 快速原型 |

---

## 🚀 方案 1: 直接加载 URDF 模型（推荐用于模拟）

### 1.1 下载 UR 机器人 URDF 文件

```bash
# 克隆官方 UR 描述包
cd frontend/public
git clone https://github.com/ros-industrial/universal_robot.git
# 或者下载简化版
wget https://github.com/gkjohnson/urdf-loaders/raw/master/urdf/T12/urdf/T12.urdf
```

### 1.2 创建 URDF 加载组件

创建 `frontend/src/components/3d/URRobot.tsx`:

```typescript
import React, { useEffect, useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { URDFLoader, URDFRobot } from 'urdf-loader';
import * as THREE from 'three';
import { useSimulatorStore } from '../../store/simulatorStore';

const URRobotComponent: React.FC = () => {
  const groupRef = useRef<THREE.Group>(null);
  const [robot, setRobot] = useState<URDFRobot | null>(null);

  const armTarget = useSimulatorStore((state) => state.armTarget);
  const gripperOpen = useSimulatorStore((state) => state.gripperOpen);

  // 加载 URDF 模型
  useEffect(() => {
    const loader = new URDFLoader();

    loader.load(
      '/universal_robot/ur_description/urdf/ur5.urdf',
      (loadedRobot) => {
        setRobot(loadedRobot);

        // 设置材质
        loadedRobot.traverse((child) => {
          if (child instanceof THREE.Mesh) {
            child.castShadow = true;
            child.receiveShadow = true;
            if (child.material) {
              (child.material as THREE.MeshStandardMaterial).metalness = 0.7;
              (child.material as THREE.MeshStandardMaterial).roughness = 0.3;
            }
          }
        });

        if (groupRef.current) {
          groupRef.current.add(loadedRobot);
        }
      },
      undefined,
      (error) => {
        console.error('Failed to load URDF:', error);
      }
    );
  }, []);

  // 更新关节角度（简化的IK - 你需要实现真实的IK库）
  useFrame(() => {
    if (robot && armTarget) {
      const [x, y, z] = armTarget;

      // 底座旋转
      robot.joints['shoulder_pan_joint']?.setJointValue(
        Math.atan2(x, z)
      );

      // 简化的肩部和肘部角度
      const dist = Math.sqrt(x * x + z * z);
      const height = y - 0.9;

      robot.joints['shoulder_lift_joint']?.setJointValue(
        -Math.atan2(height, dist) - 0.3
      );

      robot.joints['elbow_joint']?.setJointValue(
        Math.PI / 2
      );

      robot.joints['wrist_1_joint']?.setJointValue(0);
      robot.joints['wrist_2_joint']?.setJointValue(-Math.PI / 2);
      robot.joints['wrist_3_joint']?.setJointValue(0);
    }
  });

  return <group ref={groupRef} position={[0, 0, 0]} />;
};

export default URRobotComponent;
```

### 1.3 替换现有手臂

在 `Scene3D.tsx` 中:

```typescript
// 替换
import RoboticArm from './RoboticArm';
// 为
import URRobotComponent from './URRobot';

// 在场景中使用
<URRobotComponent />
```

---

## 🌉 方案 2: ROS2 Bridge 集成（真实机器人控制）

### 2.1 架构图

```
┌─────────────────┐       ┌──────────────┐       ┌─────────────┐
│   React 前端    │◄─────►│  ROS2 Bridge │◄─────►│  真实 UR5   │
│  (WebSocket)    │  JSON │  (rosbridge) │  ROS2 │   机器人    │
└─────────────────┘       └──────────────┘       └─────────────┘
```

### 2.2 后端设置（需要 ROS2）

```bash
# 安装 ROS2 Humble
# 详见: https://docs.ros.org/en/humble/Installation.html

# 安装 rosbridge
sudo apt install ros-humble-rosbridge-server

# 安装 UR 驱动
sudo apt install ros-humble-ur

# 启动 rosbridge
ros2 launch rosbridge_server rosbridge_websocket_launch.xml
```

### 2.3 前端集成

```bash
# 安装 roslib
npm install roslib
```

创建 `frontend/src/services/rosbridge.ts`:

```typescript
import ROSLIB from 'roslib';

class ROSBridge {
  private ros: ROSLIB.Ros;
  private jointStatesTopic?: ROSLIB.Topic;
  private commandTopic?: ROSLIB.Topic;

  constructor() {
    this.ros = new ROSLIB.Ros({
      url: 'ws://localhost:9090' // rosbridge 地址
    });

    this.ros.on('connection', () => {
      console.log('Connected to ROS bridge');
      this.setupTopics();
    });

    this.ros.on('error', (error) => {
      console.error('ROS bridge error:', error);
    });
  }

  private setupTopics() {
    // 订阅关节状态
    this.jointStatesTopic = new ROSLIB.Topic({
      ros: this.ros,
      name: '/joint_states',
      messageType: 'sensor_msgs/JointState'
    });

    // 发布关节命令
    this.commandTopic = new ROSLIB.Topic({
      ros: this.ros,
      name: '/scaled_joint_trajectory_controller/joint_trajectory',
      messageType: 'trajectory_msgs/JointTrajectory'
    });
  }

  moveToPosition(x: number, y: number, z: number) {
    // 调用 IK 服务
    const ikService = new ROSLIB.Service({
      ros: this.ros,
      name: '/compute_ik',
      serviceType: 'moveit_msgs/GetPositionIK'
    });

    const request = new ROSLIB.ServiceRequest({
      // IK 请求参数
    });

    ikService.callService(request, (result) => {
      // 处理结果并发送关节命令
    });
  }

  subscribeJointStates(callback: (joints: number[]) => void) {
    this.jointStatesTopic?.subscribe((message: any) => {
      callback(message.position);
    });
  }
}

export const rosBridge = new ROSBridge();
```

### 2.4 在 React 组件中使用

```typescript
import { rosBridge } from '../../services/rosbridge';

// 在组件中
useEffect(() => {
  rosBridge.subscribeJointStates((joints) => {
    // 更新 3D 模型的关节角度
    console.log('Joint angles:', joints);
  });
}, []);

// 移动机器人
const moveRobot = (x: number, y: number, z: number) => {
  rosBridge.moveToPosition(x, y, z);
};
```

---

## 🎨 方案 3: 使用 react-three/urdf (最简单)

```bash
npm install @react-three/urdf
```

```typescript
import { URDF } from '@react-three/urdf';

function Scene() {
  return (
    <Canvas>
      <URDF
        urdfPath="/models/ur5.urdf"
        onLoad={(robot) => {
          console.log('Robot loaded:', robot);
        }}
      />
    </Canvas>
  );
}
```

---

## 📊 我的建议

### 当前阶段（模拟器）
**推荐：方案 1 (URDF 加载)**
- ✅ 视觉上真实
- ✅ 不需要额外服务
- ✅ 性能好

### 未来阶段（连接真实机器人）
**升级到：方案 2 (ROS2 Bridge)**
- ✅ 真实运动学
- ✅ 可控制真实硬件
- ✅ 行业标准

---

## 🛠️ 快速开始（方案 1）

1. **下载 UR5 模型**
```bash
cd frontend/public
mkdir -p models/ur5
# 从 GitHub 下载或使用提供的模型文件
```

2. **创建组件**
```bash
# 使用上面的 URRobotComponent 代码
```

3. **测试**
```bash
npm run dev
# 访问模拟器页面，应该看到真实的 UR5 机器人
```

---

## ❓ 常见问题

**Q: URDF 文件在哪里下载？**
A:
- 官方: https://github.com/ros-industrial/universal_robot
- 示例: https://github.com/gkjohnson/urdf-loaders

**Q: 需要实现完整的 IK 吗？**
A:
- 简单模拟：可以用简化的数学公式
- 精确控制：推荐使用 IK 库如 `ikts` 或 ROS MoveIt

**Q: ROS2 Bridge 性能如何？**
A:
- 本地网络延迟 < 10ms
- 适合实时控制

---

## 📚 参考资源

- [UR URDF 模型](https://github.com/ros-industrial/universal_robot)
- [urdf-loader 文档](https://github.com/gkjohnson/urdf-loaders)
- [ROS2 Bridge](https://github.com/RobotWebTools/rosbridge_suite)
- [Universal Robots ROS2](https://github.com/UniversalRobots/Universal_Robots_ROS2_Driver)

---

需要帮助实现任何方案，随时告诉我！
