/**
 * Robotic Arm Component
 * 機械手臂組件（簡化版6DOF）
 */

import React, { useRef, useEffect } from 'react';
import { useFrame } from '@react-three/fiber';
import { Group } from 'three';
import { useSpring, animated, config } from '@react-spring/three';
import { useSimulatorStore } from '../../store/simulatorStore';

const RoboticArm: React.FC = () => {
  const armGroupRef = useRef<Group>(null);
  const shoulderRef = useRef<Group>(null);
  const elbowRef = useRef<Group>(null);
  const wristRef = useRef<Group>(null);
  const gripperRef = useRef<Group>(null);

  const armState = useSimulatorStore((state) => state.armState);
  const armTarget = useSimulatorStore((state) => state.armTarget);
  const gripperOpen = useSimulatorStore((state) => state.gripperOpen);

  // 手臂關節動畫
  const [armSpring, armSpringApi] = useSpring(() => ({
    baseRotation: 0,
    shoulderRotation: 0,
    elbowRotation: 0,
    wristRotation: 0,
    config: config.gentle,
  }));

  // 夾爪動畫
  const [gripperSpring, gripperSpringApi] = useSpring(() => ({
    openAmount: 0.3, // 0 = 閉合, 0.3 = 打開
    config: config.stiff,
  }));

  // 更新夾爪狀態
  useEffect(() => {
    gripperSpringApi.start({
      openAmount: gripperOpen ? 0.3 : 0,
    });
  }, [gripperOpen, gripperSpringApi]);

  // 改進的IK計算（2-link planar arm）
  const calculateArmAngles = (target: [number, number, number] | null) => {
    if (!target) {
      return {
        baseRotation: 0,
        shoulderRotation: 0,
        elbowRotation: 0,
        wristRotation: 0,
      };
    }

    const [x, y, z] = target;

    // 底座旋轉（朝向目標）
    const baseRotation = Math.atan2(x, z);

    // 手臂參數
    const L1 = 3.0; // 上臂長度
    const L2 = 2.4; // 前臂長度
    const baseHeight = 0.95; // 基座到肩部高度

    // 計算到目標的距離
    const horizontalDist = Math.sqrt(x * x + z * z);
    const verticalDist = y - baseHeight;

    // 計算末端到肩部的距離
    const targetDist = Math.sqrt(horizontalDist * horizontalDist + verticalDist * verticalDist);

    // 檢查是否在工作空間內
    const maxReach = L1 + L2;
    const minReach = Math.abs(L1 - L2);

    if (targetDist > maxReach || targetDist < minReach) {
      // 超出範圍，返回伸展位置
      const angle = Math.atan2(verticalDist, horizontalDist);
      return {
        baseRotation,
        shoulderRotation: angle,
        elbowRotation: 0,
        wristRotation: -angle,
      };
    }

    // 使用餘弦定理計算肘部角度
    const cosElbow = (L1 * L1 + L2 * L2 - targetDist * targetDist) / (2 * L1 * L2);
    const elbowRotation = Math.PI - Math.acos(Math.max(-1, Math.min(1, cosElbow)));

    // 計算肩部角度
    const alpha = Math.atan2(verticalDist, horizontalDist);
    const beta = Math.acos(
      Math.max(-1, Math.min(1, (L1 * L1 + targetDist * targetDist - L2 * L2) / (2 * L1 * targetDist)))
    );
    const shoulderRotation = alpha + beta;

    // 腕部角度保持末端水平
    const wristRotation = -(shoulderRotation + elbowRotation - Math.PI);

    return {
      baseRotation,
      shoulderRotation,
      elbowRotation,
      wristRotation,
    };
  };

  // 更新手臂位置
  useEffect(() => {
    if (armTarget) {
      const angles = calculateArmAngles(armTarget);
      armSpringApi.start(angles);
    }
  }, [armTarget, armSpringApi]);

  return (
    <group ref={armGroupRef} position={[0, 0, 0]}>
      {/* UR風格底座 - 圓形平台 */}
      <mesh position={[0, 0.15, 0]} castShadow>
        <cylinderGeometry args={[0.5, 0.5, 0.3, 32]} />
        <meshStandardMaterial color="#2c3e50" metalness={0.6} roughness={0.3} />
      </mesh>

      {/* UR Logo區域（深色帶） */}
      <mesh position={[0, 0.32, 0]}>
        <cylinderGeometry args={[0.51, 0.51, 0.05, 32]} />
        <meshStandardMaterial color="#1a252f" metalness={0.5} />
      </mesh>

      {/* 旋轉底座（Joint 0） */}
      <animated.group rotation-y={armSpring.baseRotation} position={[0, 0.35, 0]}>
        {/* UR典型的圓柱形關節 */}
        <mesh castShadow>
          <cylinderGeometry args={[0.35, 0.35, 0.4, 32]} />
          <meshStandardMaterial color="#34495e" metalness={0.7} roughness={0.2} />
        </mesh>

        {/* 關節連接環 */}
        <mesh position={[0, 0.2, 0]}>
          <torusGeometry args={[0.36, 0.03, 16, 32]} />
          <meshStandardMaterial color="#1a252f" metalness={0.8} />
        </mesh>

        {/* 肩部關節（Joint 1） - UR風格 */}
        <animated.group
          ref={shoulderRef}
          position={[0, 0.6, 0]}
          rotation-z={armSpring.shoulderRotation}
        >
          {/* 肩部圓柱關節 */}
          <mesh castShadow rotation={[Math.PI / 2, 0, 0]}>
            <cylinderGeometry args={[0.3, 0.3, 0.5, 32]} />
            <meshStandardMaterial color="#34495e" metalness={0.7} roughness={0.2} />
          </mesh>

          {/* 關節裝飾環 */}
          <mesh rotation={[Math.PI / 2, 0, 0]}>
            <torusGeometry args={[0.31, 0.02, 16, 32]} />
            <meshStandardMaterial color="#1a252f" metalness={0.8} />
          </mesh>

          {/* 上臂段（Link 1） - UR特徵圓柱設計 */}
          <group position={[0, 1.5, 0]}>
            <mesh castShadow>
              <cylinderGeometry args={[0.2, 0.2, 3, 32]} />
              <meshStandardMaterial color="#34495e" metalness={0.7} roughness={0.2} />
            </mesh>

            {/* 上臂裝飾條紋 */}
            {[0.5, 1.5, 2.5].map((y, i) => (
              <mesh key={i} position={[0, y - 1.5, 0]}>
                <cylinderGeometry args={[0.21, 0.21, 0.08, 32]} />
                <meshStandardMaterial color="#2c3e50" metalness={0.6} />
              </mesh>
            ))}
          </group>

          {/* 肘部關節（Joint 2） */}
          <animated.group
            ref={elbowRef}
            position={[0, 3, 0]}
            rotation-z={armSpring.elbowRotation}
          >
            {/* 肘部圓柱關節 */}
            <mesh castShadow rotation={[Math.PI / 2, 0, 0]}>
              <cylinderGeometry args={[0.25, 0.25, 0.4, 32]} />
              <meshStandardMaterial color="#34495e" metalness={0.7} roughness={0.2} />
            </mesh>

            {/* 關節裝飾環 */}
            <mesh rotation={[Math.PI / 2, 0, 0]}>
              <torusGeometry args={[0.26, 0.02, 16, 32]} />
              <meshStandardMaterial color="#1a252f" metalness={0.8} />
            </mesh>

            {/* 前臂段（Link 2） */}
            <group position={[0, 1.2, 0]}>
              <mesh castShadow>
                <cylinderGeometry args={[0.18, 0.18, 2.4, 32]} />
                <meshStandardMaterial color="#34495e" metalness={0.7} roughness={0.2} />
              </mesh>

              {/* 前臂裝飾條紋 */}
              {[0.4, 1.2, 2].map((y, i) => (
                <mesh key={i} position={[0, y - 1.2, 0]}>
                  <cylinderGeometry args={[0.19, 0.19, 0.06, 32]} />
                  <meshStandardMaterial color="#2c3e50" metalness={0.6} />
                </mesh>
              ))}
            </group>

            {/* 腕部關節組（Joint 3, 4, 5） */}
            <animated.group
              ref={wristRef}
              position={[0, 2.4, 0]}
              rotation-z={armSpring.wristRotation}
            >
              {/* 腕部關節1（Joint 3） */}
              <mesh castShadow rotation={[Math.PI / 2, 0, 0]}>
                <cylinderGeometry args={[0.15, 0.15, 0.3, 32]} />
                <meshStandardMaterial color="#34495e" metalness={0.7} roughness={0.2} />
              </mesh>

              {/* 腕部連接段 */}
              <mesh position={[0, 0.3, 0]} castShadow>
                <cylinderGeometry args={[0.12, 0.12, 0.6, 32]} />
                <meshStandardMaterial color="#2c3e50" metalness={0.6} />
              </mesh>

              {/* 腕部關節2（Joint 4） */}
              <mesh position={[0, 0.6, 0]} castShadow>
                <cylinderGeometry args={[0.12, 0.12, 0.2, 32]} />
                <meshStandardMaterial color="#34495e" metalness={0.7} />
              </mesh>

              {/* 法蘭盤 */}
              <mesh position={[0, 0.8, 0]} castShadow>
                <cylinderGeometry args={[0.15, 0.12, 0.1, 32]} />
                <meshStandardMaterial color="#2c3e50" metalness={0.8} />
              </mesh>

              {/* 末端執行器底座 */}
              <mesh position={[0, 0.9, 0]} castShadow>
                <cylinderGeometry args={[0.18, 0.15, 0.15, 6]} />
                <meshStandardMaterial color="#1a252f" metalness={0.9} />
              </mesh>

              {/* 吸嘴組件 - 真空吸盤 */}
              <animated.group ref={gripperRef} position={[0, 1.1, 0]}>
                {/* 吸嘴連接座 */}
                <mesh castShadow>
                  <cylinderGeometry args={[0.12, 0.15, 0.15, 16]} />
                  <meshStandardMaterial color="#2c3e50" metalness={0.8} />
                </mesh>

                {/* 吸嘴管 */}
                <mesh position={[0, -0.15, 0]} castShadow>
                  <cylinderGeometry args={[0.08, 0.08, 0.3, 16]} />
                  <meshStandardMaterial color="#34495e" metalness={0.7} />
                </mesh>

                {/* 波紋管段 */}
                {[...Array(3)].map((_, i) => (
                  <mesh key={i} position={[0, -0.35 - i * 0.05, 0]}>
                    <cylinderGeometry args={[0.1, 0.1, 0.03, 16]} />
                    <meshStandardMaterial color="#1a252f" metalness={0.6} />
                  </mesh>
                ))}

                {/* 吸盤本體 */}
                <mesh position={[0, -0.55, 0]} castShadow>
                  <cylinderGeometry args={[0.15, 0.12, 0.08, 32]} />
                  <meshStandardMaterial color="#1a1a1a" roughness={0.9} metalness={0.1} />
                </mesh>

                {/* 吸盤底部（橡膠） */}
                <mesh position={[0, -0.6, 0]}>
                  <cylinderGeometry args={[0.16, 0.15, 0.04, 32]} />
                  <meshStandardMaterial
                    color={gripperOpen ? '#333333' : '#ff6600'}
                    roughness={0.95}
                    emissive={gripperOpen ? '#000000' : '#ff6600'}
                    emissiveIntensity={gripperOpen ? 0 : 0.3}
                  />
                </mesh>

                {/* 吸盤內部環 */}
                <mesh position={[0, -0.62, 0]}>
                  <torusGeometry args={[0.1, 0.015, 16, 32]} />
                  <meshStandardMaterial color="#ff6600" metalness={0.5} />
                </mesh>

                {/* 真空指示燈 */}
                <mesh position={[0.12, -0.25, 0]}>
                  <sphereGeometry args={[0.02, 16, 16]} />
                  <meshStandardMaterial
                    color={gripperOpen ? '#00ff00' : '#ff0000'}
                    emissive={gripperOpen ? '#00ff00' : '#ff0000'}
                    emissiveIntensity={1.5}
                  />
                </mesh>

                {/* 氣管連接 */}
                <mesh position={[0.08, 0, 0]} rotation={[0, 0, Math.PI / 2]}>
                  <cylinderGeometry args={[0.015, 0.015, 0.1, 8]} />
                  <meshStandardMaterial color="#0066cc" metalness={0.4} />
                </mesh>
              </animated.group>
            </animated.group>
          </animated.group>
        </animated.group>
      </animated.group>

      {/* 相機模擬（檢測裝置） */}
      <mesh position={[0, 3.5, 0.8]} castShadow>
        <boxGeometry args={[0.3, 0.2, 0.2]} />
        <meshStandardMaterial color="#000000" metalness={0.9} />
      </mesh>

      {/* 相機鏡頭 */}
      <mesh position={[0, 3.5, 0.9]} rotation={[Math.PI / 2, 0, 0]}>
        <cylinderGeometry args={[0.08, 0.08, 0.15, 16]} />
        <meshStandardMaterial color="#333333" metalness={1} />
      </mesh>

      {/* 指示燈（根據狀態變色） */}
      <mesh position={[0, 0.8, 0.3]}>
        <sphereGeometry args={[0.05, 16, 16]} />
        <meshStandardMaterial
          color={
            armState === 'idle'
              ? '#00ff00'
              : armState === 'gripping'
              ? '#ffff00'
              : '#ff0000'
          }
          emissive={
            armState === 'idle'
              ? '#00ff00'
              : armState === 'gripping'
              ? '#ffff00'
              : '#ff0000'
          }
          emissiveIntensity={2}
        />
      </mesh>
    </group>
  );
};

export default RoboticArm;
