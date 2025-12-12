/**
 * Virtual Camera Component
 * 虛擬相機組件 - 用於手臂端的相機視角
 */

import React, { useRef, useMemo } from 'react';
import { useFrame, useThree, createPortal } from '@react-three/fiber';
import * as THREE from 'three';
import { PerspectiveCamera, useFBO } from '@react-three/drei';
import { useSimulatorStore } from '../../store/simulatorStore';

interface VirtualCameraProps {
  onTextureUpdate?: (texture: THREE.Texture) => void;
}

const VirtualCamera: React.FC<VirtualCameraProps> = ({ onTextureUpdate }) => {
  const cameraRef = useRef<THREE.PerspectiveCamera>(null);
  const { scene, gl } = useThree();

  // 創建渲染目標
  const renderTarget = useFBO(512, 384); // 4:3 比例

  // 創建虛擬場景用於渲染相機視角
  const virtualScene = useMemo(() => new THREE.Scene(), []);

  useFrame(() => {
    if (!cameraRef.current) return;

    // 相機位置在手臂上方，俯視檢測區域
    cameraRef.current.position.set(0, 3.8, 0.8);
    cameraRef.current.lookAt(2, 0.3, 0);

    // 將主場景的物體渲染到相機視角
    const currentRenderTarget = gl.getRenderTarget();

    // 渲染到紋理
    gl.setRenderTarget(renderTarget);
    gl.render(scene, cameraRef.current);
    gl.setRenderTarget(currentRenderTarget);

    // 通知父組件紋理已更新
    if (onTextureUpdate) {
      onTextureUpdate(renderTarget.texture);
    }
  });

  return (
    <>
      {/* 虛擬相機 */}
      <PerspectiveCamera ref={cameraRef} fov={60} position={[0, 3.8, 0.8]} />

      {/* 相機可視化（調試用） */}
      <mesh position={[0, 3.8, 0.8]} visible={false}>
        <boxGeometry args={[0.2, 0.15, 0.15]} />
        <meshStandardMaterial color="#ff0000" />
      </mesh>
    </>
  );
};

export default VirtualCamera;
