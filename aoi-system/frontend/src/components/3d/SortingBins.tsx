/**
 * Sorting Bins Component
 * 分揀容器（正確區/錯誤區）
 */

import React from 'react';
import { Text } from '@react-three/drei';

interface BinProps {
  position: [number, number, number];
  color: string;
  label: string;
  labelColor: string;
}

const Bin: React.FC<BinProps> = ({ position, color, label, labelColor }) => {
  return (
    <group position={position}>
      {/* 容器底部 */}
      <mesh position={[0, 0, 0]} receiveShadow>
        <boxGeometry args={[2, 0.1, 2]} />
        <meshStandardMaterial color="#666666" metalness={0.5} />
      </mesh>

      {/* 容器四周 */}
      {/* 前牆 */}
      <mesh position={[0, 0.5, 1]} castShadow>
        <boxGeometry args={[2, 1, 0.1]} />
        <meshStandardMaterial
          color={color}
          transparent
          opacity={0.3}
          metalness={0.2}
        />
      </mesh>

      {/* 後牆 */}
      <mesh position={[0, 0.5, -1]} castShadow>
        <boxGeometry args={[2, 1, 0.1]} />
        <meshStandardMaterial
          color={color}
          transparent
          opacity={0.3}
          metalness={0.2}
        />
      </mesh>

      {/* 左牆 */}
      <mesh position={[-1, 0.5, 0]} castShadow>
        <boxGeometry args={[0.1, 1, 2]} />
        <meshStandardMaterial
          color={color}
          transparent
          opacity={0.3}
          metalness={0.2}
        />
      </mesh>

      {/* 右牆 */}
      <mesh position={[1, 0.5, 0]} castShadow>
        <boxGeometry args={[0.1, 1, 2]} />
        <meshStandardMaterial
          color={color}
          transparent
          opacity={0.3}
          metalness={0.2}
        />
      </mesh>

      {/* 標籤 */}
      <Text
        position={[0, 1.2, 0]}
        fontSize={0.4}
        color={labelColor}
        anchorX="center"
        anchorY="middle"
      >
        {label}
      </Text>

      {/* 底部發光效果 */}
      <mesh position={[0, 0.05, 0]}>
        <cylinderGeometry args={[0.9, 0.9, 0.05, 32]} />
        <meshBasicMaterial
          color={color}
          transparent
          opacity={0.2}
        />
      </mesh>
    </group>
  );
};

const SortingBins: React.FC = () => {
  return (
    <group>
      {/* 正確區（PASS） */}
      <Bin
        position={[-3, 0.05, -3]}
        color="#00ff00"
        label="✓ PASS"
        labelColor="#00ff00"
      />

      {/* 錯誤區（NG） */}
      <Bin
        position={[3, 0.05, -3]}
        color="#ff0000"
        label="✗ NG"
        labelColor="#ff0000"
      />

      {/* 地面標示 - PASS */}
      <mesh position={[-3, 0.01, -3]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[1.5, 2, 32]} />
        <meshBasicMaterial color="#00ff00" transparent opacity={0.1} />
      </mesh>

      {/* 地面標示 - NG */}
      <mesh position={[3, 0.01, -3]} rotation={[-Math.PI / 2, 0, 0]}>
        <ringGeometry args={[1.5, 2, 32]} />
        <meshBasicMaterial color="#ff0000" transparent opacity={0.1} />
      </mesh>
    </group>
  );
};

export default SortingBins;
