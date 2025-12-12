/**
 * Conveyor Belt Component
 * 傳送帶組件
 */

import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Mesh, CanvasTexture, RepeatWrapping } from 'three';
import { useSimulatorStore } from '../../store/simulatorStore';

const ConveyorBelt: React.FC = () => {
  const meshRef = useRef<Mesh>(null);
  const materialRef = useRef<any>(null);

  const isRunning = useSimulatorStore((state) => state.isRunning);
  const isPaused = useSimulatorStore((state) => state.isPaused);
  const speed = useSimulatorStore((state) => state.speed);

  // 創建傳送帶紋理
  const beltTexture = useMemo(() => {
    const canvas = document.createElement('canvas');
    canvas.width = 256;
    canvas.height = 256;
    const ctx = canvas.getContext('2d')!;

    // 繪製深色背景
    ctx.fillStyle = '#2c2c2c';
    ctx.fillRect(0, 0, 256, 256);

    // 繪製橫向條紋（傳送帶紋路）
    ctx.fillStyle = '#1a1a1a';
    for (let i = 0; i < 256; i += 16) {
      ctx.fillRect(0, i, 256, 4);
    }

    // 繪製細微的磨損紋理
    for (let i = 0; i < 100; i++) {
      ctx.fillStyle = `rgba(${Math.random() * 50}, ${Math.random() * 50}, ${Math.random() * 50}, 0.3)`;
      ctx.fillRect(Math.random() * 256, Math.random() * 256, 2, 2);
    }

    const texture = new CanvasTexture(canvas);
    texture.wrapS = texture.wrapT = RepeatWrapping;
    texture.repeat.set(4, 1);

    return texture;
  }, []);

  // 動畫：移動紋理模擬傳送帶運動
  useFrame((state, delta) => {
    if (materialRef.current?.map && isRunning && !isPaused) {
      materialRef.current.map.offset.x -= delta * 0.1 * speed;
    }
  });

  return (
    <group position={[2, 0.1, 0]}>
      {/* 傳送帶主體 */}
      <mesh ref={meshRef} receiveShadow castShadow>
        <boxGeometry args={[8, 0.2, 2]} />
        <meshStandardMaterial
          ref={materialRef}
          map={beltTexture}
          color="#2c2c2c"
          metalness={0.4}
          roughness={0.6}
        />
      </mesh>

      {/* 傳送帶側邊 */}
      <mesh position={[0, 0.3, 1.1]} castShadow>
        <boxGeometry args={[8, 0.4, 0.1]} />
        <meshStandardMaterial color="#1a1a1a" metalness={0.8} />
      </mesh>

      <mesh position={[0, 0.3, -1.1]} castShadow>
        <boxGeometry args={[8, 0.4, 0.1]} />
        <meshStandardMaterial color="#1a1a1a" metalness={0.8} />
      </mesh>

      {/* 支撐架 */}
      <mesh position={[-3, -0.5, 1]} castShadow>
        <cylinderGeometry args={[0.05, 0.05, 1, 8]} />
        <meshStandardMaterial color="#333333" metalness={0.9} />
      </mesh>

      <mesh position={[-3, -0.5, -1]} castShadow>
        <cylinderGeometry args={[0.05, 0.05, 1, 8]} />
        <meshStandardMaterial color="#333333" metalness={0.9} />
      </mesh>

      <mesh position={[3, -0.5, 1]} castShadow>
        <cylinderGeometry args={[0.05, 0.05, 1, 8]} />
        <meshStandardMaterial color="#333333" metalness={0.9} />
      </mesh>

      <mesh position={[3, -0.5, -1]} castShadow>
        <cylinderGeometry args={[0.05, 0.05, 1, 8]} />
        <meshStandardMaterial color="#333333" metalness={0.9} />
      </mesh>

      {/* 檢測標記位置 */}
      <mesh position={[0, 0.25, 0]}>
        <cylinderGeometry args={[0.4, 0.4, 0.05, 32]} />
        <meshStandardMaterial
          color="#ffff00"
          transparent
          opacity={0.3}
          emissive="#ffff00"
          emissiveIntensity={0.5}
        />
      </mesh>

      {/* 檢測區域標示 */}
      <mesh position={[0, 2, 0]} rotation={[Math.PI / 2, 0, 0]}>
        <ringGeometry args={[0.6, 0.8, 32]} />
        <meshBasicMaterial color="#00ff00" transparent opacity={0.2} />
      </mesh>
    </group>
  );
};

export default ConveyorBelt;
