/**
 * Main 3D Scene Component
 * 主要3D場景容器
 */

import React, { Suspense, useState, createContext, useContext } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Grid, PerspectiveCamera, View } from '@react-three/drei';
import { Box, CircularProgress } from '@mui/material';
import { useSimulatorStore } from '../../store/simulatorStore';

// 创建 Context 用于共享相机容器
export const ArmCameraContext = createContext<HTMLDivElement | null>(null);

// 子組件（稍後實作）
import RoboticArm from './RoboticArm';
import ConveyorBelt from './ConveyorBelt';
import SortingBins from './SortingBins';
import WorkPieces from './WorkPieces';
import Lighting from './Lighting';

const Scene3D: React.FC = () => {
  const cameraView = useSimulatorStore((state) => state.cameraView);
  const [isLoading, setIsLoading] = useState(true);

  // 相機預設位置
  const getCameraPosition = (): [number, number, number] => {
    switch (cameraView) {
      case 'top':
        return [0, 10, 0];
      case 'side':
        return [10, 5, 0];
      case 'front':
        return [0, 5, 10];
      case 'free':
      default:
        return [8, 8, 8];
    }
  };

  return (
    <Box
      sx={{
        width: '100%',
        height: '600px',
        position: 'relative',
        bgcolor: '#1a1a1a',
        borderRadius: 2,
        overflow: 'hidden',
      }}
    >
      <Canvas
        shadows
        camera={{
          position: getCameraPosition(),
          fov: 50,
        }}
        onCreated={() => setIsLoading(false)}
      >
        <Suspense fallback={null}>
          {/* 光源 */}
          <Lighting />

          {/* 網格地板 */}
          <Grid
            args={[20, 20]}
            cellSize={1}
            cellThickness={0.5}
            cellColor="#6e6e6e"
            sectionSize={5}
            sectionThickness={1}
            sectionColor="#9d9d9d"
            fadeDistance={30}
            fadeStrength={1}
            followCamera={false}
            infiniteGrid={false}
            position={[0, -0.01, 0]}
          />

          {/* 工作台底座 - 改進材質 */}
          <mesh position={[0, -0.5, 0]} receiveShadow>
            <boxGeometry args={[12, 0.5, 8]} />
            <meshStandardMaterial
              color="#d0d0d0"
              metalness={0.3}
              roughness={0.7}
            />
          </mesh>

          {/* 工作台邊框 */}
          <mesh position={[6, -0.25, 0]}>
            <boxGeometry args={[0.1, 0.5, 8]} />
            <meshStandardMaterial color="#555555" metalness={0.8} />
          </mesh>
          <mesh position={[-6, -0.25, 0]}>
            <boxGeometry args={[0.1, 0.5, 8]} />
            <meshStandardMaterial color="#555555" metalness={0.8} />
          </mesh>
          <mesh position={[0, -0.25, 4]}>
            <boxGeometry args={[12, 0.5, 0.1]} />
            <meshStandardMaterial color="#555555" metalness={0.8} />
          </mesh>
          <mesh position={[0, -0.25, -4]}>
            <boxGeometry args={[12, 0.5, 0.1]} />
            <meshStandardMaterial color="#555555" metalness={0.8} />
          </mesh>

          {/* 背景牆壁 */}
          <mesh position={[0, 3, -5]} receiveShadow>
            <planeGeometry args={[15, 8]} />
            <meshStandardMaterial
              color="#f5f5f5"
              roughness={0.9}
            />
          </mesh>

          {/* 側牆 */}
          <mesh position={[-7.5, 3, 0]} rotation={[0, Math.PI / 2, 0]} receiveShadow>
            <planeGeometry args={[10, 8]} />
            <meshStandardMaterial
              color="#f0f0f0"
              roughness={0.9}
            />
          </mesh>

          {/* 傳送帶 */}
          <ConveyorBelt />

          {/* 機械手臂 */}
          <RoboticArm />

          {/* 分揀容器 */}
          <SortingBins />

          {/* 待檢物件 */}
          <WorkPieces />

          {/* 相機控制 */}
          <OrbitControls
            enablePan={cameraView === 'free'}
            enableRotate={cameraView === 'free'}
            enableZoom={true}
            minDistance={5}
            maxDistance={30}
            maxPolarAngle={Math.PI / 2}
          />
        </Suspense>
      </Canvas>

      {/* 載入提示 */}
      {isLoading && (
        <Box
          sx={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            pointerEvents: 'none',
          }}
        >
          <CircularProgress />
        </Box>
      )}
    </Box>
  );
};

export default Scene3D;
