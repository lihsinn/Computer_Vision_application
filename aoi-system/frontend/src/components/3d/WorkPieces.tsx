/**
 * Work Pieces Component
 * 待檢物件組件
 */

import React, { useRef, useEffect } from 'react';
import { useSpring, animated } from '@react-spring/three';
import { useFrame, useThree } from '@react-three/fiber';
import { Group, Vector3 } from 'three';
import { useSimulatorStore } from '../../store/simulatorStore';

interface SinglePieceProps {
  id: string;
  position: [number, number, number];
  rotation: [number, number, number];
  status: 'queue' | 'detecting' | 'gripped' | 'sorted' | 'completed';
  detectionResult?: 'PASS' | 'NG';
}

const SinglePiece: React.FC<SinglePieceProps> = ({
  id,
  position,
  rotation,
  status,
  detectionResult,
}) => {
  const groupRef = useRef<Group>(null);
  const { scene } = useThree();
  const armTarget = useSimulatorStore((state) => state.armTarget);

  // 動畫控制位置（僅在未被抓取時使用）
  const spring = useSpring({
    position: status === 'gripped' ? position : position,
    rotation,
    config: { tension: 120, friction: 14 },
  });

  // 當物體被抓取時，跟隨手臂末端
  useFrame(() => {
    if (status === 'gripped' && armTarget && groupRef.current) {
      // 物體應該在手臂末端下方一點點（吸附位置）
      const targetPos = new Vector3(armTarget[0], armTarget[1] - 0.8, armTarget[2]);

      // 平滑插值到目標位置
      groupRef.current.position.lerp(targetPos, 0.15);
    }
  });

  // 根據狀態決定顏色
  const getColor = () => {
    if (status === 'completed') {
      return detectionResult === 'PASS' ? '#00ff00' : '#ff0000';
    }
    if (status === 'detecting') {
      return '#ffff00';
    }
    return '#888888';
  };

  // 根據狀態決定是否發光
  const getEmissive = () => {
    if (status === 'detecting') {
      return '#ffff00';
    }
    if (status === 'completed') {
      return detectionResult === 'PASS' ? '#00ff00' : '#ff0000';
    }
    return '#000000';
  };

  return (
    <animated.group
      ref={groupRef}
      position={status !== 'gripped' ? spring.position : undefined}
      rotation={spring.rotation}
    >
      {/* 主體（螺絲/零件） */}
      <mesh castShadow receiveShadow>
        <cylinderGeometry args={[0.15, 0.15, 0.4, 16]} />
        <meshStandardMaterial
          color={getColor()}
          metalness={0.8}
          roughness={0.3}
          emissive={getEmissive()}
          emissiveIntensity={0.3}
        />
      </mesh>

      {/* 螺絲頭 */}
      <mesh position={[0, 0.25, 0]} castShadow>
        <cylinderGeometry args={[0.2, 0.15, 0.1, 16]} />
        <meshStandardMaterial
          color={getColor()}
          metalness={0.9}
          roughness={0.2}
        />
      </mesh>

      {/* 螺紋紋路（裝飾） */}
      {[...Array(6)].map((_, i) => (
        <mesh
          key={i}
          position={[0, -0.15 + i * 0.06, 0]}
          rotation={[0, (i * Math.PI) / 4, 0]}
        >
          <torusGeometry args={[0.16, 0.01, 8, 16]} />
          <meshStandardMaterial color="#555555" metalness={0.5} />
        </mesh>
      ))}

      {/* 檢測中的標記 */}
      {status === 'detecting' && (
        <mesh position={[0, 0.6, 0]}>
          <ringGeometry args={[0.2, 0.3, 32]} />
          <meshBasicMaterial color="#ffff00" transparent opacity={0.6} />
        </mesh>
      )}
    </animated.group>
  );
};

const WorkPieces: React.FC = () => {
  const workPieces = useSimulatorStore((state) => state.workPieces);

  return (
    <group>
      {workPieces.map((piece) => (
        <SinglePiece
          key={piece.id}
          id={piece.id}
          position={piece.position}
          rotation={piece.rotation}
          status={piece.status}
          detectionResult={piece.detectionResult}
        />
      ))}
    </group>
  );
};

export default WorkPieces;
