/**
 * Camera View Component
 * 手臂相机视角组件 - 显示检测画面和瑕疵标注
 */

import React, { useState, useEffect, useRef } from 'react';
import { Box, Paper, Typography, Chip } from '@mui/material';
import { CameraAlt as CameraIcon } from '@mui/icons-material';
import { Canvas } from '@react-three/fiber';
import { useSimulatorStore } from '../store/simulatorStore';
import * as THREE from 'three';

interface DefectAnnotation {
  id: string;
  x: number; // 0-1
  y: number; // 0-1
  width: number;
  height: number;
  type: string;
  confidence: number;
}

// 內部組件：顯示相機渲染紋理
const CameraRenderer: React.FC<{ texture: THREE.Texture | null }> = ({ texture }) => {
  return (
    <mesh>
      <planeGeometry args={[2, 1.5]} />
      <meshBasicMaterial map={texture} />
    </mesh>
  );
};

const CameraView: React.FC = () => {
  const currentWorkPiece = useSimulatorStore((state) => state.currentWorkPiece);
  const armState = useSimulatorStore((state) => state.armState);

  const [isCapturing, setIsCapturing] = useState(false);
  const [defects, setDefects] = useState<DefectAnnotation[]>([]);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // 模拟拍照和检测
  useEffect(() => {
    if (armState === 'detecting') {
      setIsCapturing(true);

      // 模拟拍照延迟
      setTimeout(() => {
        setIsCapturing(false);

        // 模拟检测瑕疵（随机生成）
        const shouldHaveDefect = Math.random() > 0.3;

        if (shouldHaveDefect) {
          // 生成1-3个瑕疵
          const numDefects = Math.floor(Math.random() * 3) + 1;
          const newDefects: DefectAnnotation[] = [];

          for (let i = 0; i < numDefects; i++) {
            newDefects.push({
              id: `defect-${Date.now()}-${i}`,
              x: Math.random() * 0.6 + 0.2,
              y: Math.random() * 0.6 + 0.2,
              width: Math.random() * 0.15 + 0.05,
              height: Math.random() * 0.15 + 0.05,
              type: ['刮痕', '凹陷', '污漬', '變形'][Math.floor(Math.random() * 4)],
              confidence: Math.random() * 0.3 + 0.7,
            });
          }

          setDefects(newDefects);
        } else {
          setDefects([]);
        }
      }, 800);
    } else {
      // 清空瑕疵标注
      if (armState === 'idle') {
        setDefects([]);
      }
    }
  }, [armState]);

  // 计算瑕疵标注的绝对位置
  const getDefectStyle = (defect: DefectAnnotation) => {
    return {
      position: 'absolute' as const,
      left: `${defect.x * 100}%`,
      top: `${defect.y * 100}%`,
      width: `${defect.width * 100}%`,
      height: `${defect.height * 100}%`,
      border: '2px solid #ff0000',
      borderRadius: '4px',
      pointerEvents: 'none' as const,
      animation: 'blink 1s infinite',
    };
  };

  return (
    <Paper sx={{ p: 2, height: '100%' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <CameraIcon sx={{ mr: 1 }} />
        <Typography variant="h6">手臂相機視角</Typography>
        {isCapturing && (
          <Chip
            label="拍攝中..."
            color="warning"
            size="small"
            sx={{ ml: 2 }}
          />
        )}
        {armState === 'detecting' && !isCapturing && (
          <Chip
            label="檢測中..."
            color="info"
            size="small"
            sx={{ ml: 2 }}
          />
        )}
      </Box>

      {/* 相機畫面 */}
      <Box
        sx={{
          position: 'relative',
          width: '100%',
          paddingTop: '75%', // 4:3 比例
          bgcolor: '#1a1a1a',
          borderRadius: 2,
          overflow: 'hidden',
          border: '2px solid #333',
        }}
      >
        {/* Three.js Canvas 渲染相機視角 */}
        <Canvas
          ref={canvasRef}
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
          }}
          camera={{ position: [0, 0, 2], fov: 50 }}
          gl={{ preserveDrawingBuffer: true }}
        >
          {/* 增強光照 - 模擬相機補光燈 */}
          <ambientLight intensity={1.2} />
          <directionalLight position={[0, 5, 0]} intensity={2.5} />
          <pointLight position={[2, 3, 2]} intensity={1.5} />
          <pointLight position={[-2, 3, -2]} intensity={1.0} />

          {/* 顯示檢測區域的俯視圖 - 優化角度 */}
          <group rotation={[-Math.PI / 2.2, 0, 0]} position={[0, -0.2, 0]}>
            {/* 傳送帶背景 - 更真實 */}
            <mesh>
              <planeGeometry args={[4, 3]} />
              <meshStandardMaterial color="#3a3a3a" roughness={0.6} metalness={0.2} />
            </mesh>

            {/* 檢測區域標記 */}
            <mesh position={[0, 0, 0.02]}>
              <ringGeometry args={[0.5, 0.6, 32]} />
              <meshBasicMaterial color="#00ff00" transparent opacity={0.5} />
            </mesh>

            {/* 如果有當前工件，顯示工件 - 更亮的材質 */}
            {currentWorkPiece && (
              <group position={[0, 0, 0.15]} rotation={[0, 0, Math.PI / 2]}>
                {/* 螺絲主體 */}
                <mesh castShadow>
                  <cylinderGeometry args={[0.18, 0.18, 0.5, 16]} />
                  <meshStandardMaterial
                    color="#c0c0c0"
                    metalness={0.9}
                    roughness={0.2}
                    emissive="#404040"
                    emissiveIntensity={0.2}
                  />
                </mesh>
                {/* 螺絲頭 */}
                <mesh position={[0, 0.3, 0]} castShadow>
                  <cylinderGeometry args={[0.24, 0.18, 0.12, 16]} />
                  <meshStandardMaterial
                    color="#d0d0d0"
                    metalness={0.95}
                    roughness={0.15}
                  />
                </mesh>
                {/* 螺紋 */}
                {[...Array(6)].map((_, i) => (
                  <mesh
                    key={i}
                    position={[0, -0.2 + i * 0.08, 0]}
                    rotation={[0, (i * Math.PI) / 4, 0]}
                  >
                    <torusGeometry args={[0.19, 0.015, 8, 16]} />
                    <meshStandardMaterial color="#808080" metalness={0.7} />
                  </mesh>
                ))}
              </group>
            )}
          </group>
        </Canvas>

        {/* 十字準線 */}
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            pointerEvents: 'none',
          }}
        >
          {/* 水平線 */}
          <Box
            sx={{
              position: 'absolute',
              top: '50%',
              left: 0,
              right: 0,
              height: '1px',
              bgcolor: '#00ff00',
              opacity: 0.3,
            }}
          />
          {/* 垂直線 */}
          <Box
            sx={{
              position: 'absolute',
              left: '50%',
              top: 0,
              bottom: 0,
              width: '1px',
              bgcolor: '#00ff00',
              opacity: 0.3,
            }}
          />
          {/* 中心點 */}
          <Box
            sx={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              width: '20px',
              height: '20px',
              border: '2px solid #00ff00',
              borderRadius: '50%',
              opacity: 0.5,
            }}
          />
        </Box>

        {/* 瑕疵標注 */}
        {defects.map((defect) => (
          <Box key={defect.id}>
            <Box sx={getDefectStyle(defect)} />
            <Box
              sx={{
                position: 'absolute',
                left: `${defect.x * 100}%`,
                top: `${(defect.y - 0.08) * 100}%`,
                transform: 'translateX(-50%)',
                bgcolor: 'rgba(255, 0, 0, 0.8)',
                color: 'white',
                padding: '2px 6px',
                borderRadius: '4px',
                fontSize: '10px',
                whiteSpace: 'nowrap',
                pointerEvents: 'none',
              }}
            >
              {defect.type} ({(defect.confidence * 100).toFixed(0)}%)
            </Box>
          </Box>
        ))}

        {/* 拍照閃光效果 */}
        {isCapturing && (
          <Box
            sx={{
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              bgcolor: 'white',
              opacity: 0.8,
              animation: 'flash 0.3s ease-out',
            }}
          />
        )}

        {/* 狀態資訊 */}
        <Box
          sx={{
            position: 'absolute',
            bottom: 8,
            left: 8,
            right: 8,
            display: 'flex',
            justifyContent: 'space-between',
            color: '#00ff00',
            fontSize: '12px',
            fontFamily: 'monospace',
          }}
        >
          <span>● REC</span>
          <span>{new Date().toLocaleTimeString()}</span>
        </Box>
      </Box>

      {/* 檢測結果 */}
      {defects.length > 0 && (
        <Box sx={{ mt: 2 }}>
          <Typography variant="body2" color="error" gutterBottom>
            檢測到 {defects.length} 個瑕疵：
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
            {defects.map((defect) => (
              <Chip
                key={defect.id}
                label={`${defect.type} (${(defect.confidence * 100).toFixed(0)}%)`}
                size="small"
                color="error"
                variant="outlined"
              />
            ))}
          </Box>
        </Box>
      )}

      {/* CSS 動畫 */}
      <style>
        {`
          @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
          }
          @keyframes flash {
            0% { opacity: 0; }
            50% { opacity: 0.8; }
            100% { opacity: 0; }
          }
        `}
      </style>
    </Paper>
  );
};

export default CameraView;
