/**
 * Lighting Component
 * 場景光源設置
 */

import React from 'react';

const Lighting: React.FC = () => {
  return (
    <>
      {/* 環境光 - 增加亮度 */}
      <ambientLight intensity={0.8} />

      {/* 主要方向光 - 增加亮度 */}
      <directionalLight
        position={[10, 10, 5]}
        intensity={1.8}
        castShadow
        shadow-mapSize-width={2048}
        shadow-mapSize-height={2048}
        shadow-camera-far={50}
        shadow-camera-left={-10}
        shadow-camera-right={10}
        shadow-camera-top={10}
        shadow-camera-bottom={-10}
      />

      {/* 補光 - 增加亮度 */}
      <directionalLight position={[-5, 5, -5]} intensity={0.8} />
      <directionalLight position={[5, 5, 5]} intensity={0.6} />

      {/* 聚光燈（檢測區域） - 增加亮度 */}
      <spotLight
        position={[0, 8, 0]}
        angle={0.3}
        penumbra={0.5}
        intensity={1.5}
        castShadow
        color="#ffffff"
      />

      {/* 底部反射光 - 增加亮度 */}
      <hemisphereLight
        skyColor="#ffffff"
        groundColor="#888888"
        intensity={0.5}
      />
    </>
  );
};

export default Lighting;
