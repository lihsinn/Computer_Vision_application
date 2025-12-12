/**
 * Robotic Arm Simulator Page
 * 3D機械手臂智能分揀模擬器主頁面
 */

import React, { useEffect, useRef } from 'react';
import {
  Box,
  Container,
  Grid,
  Paper,
  Typography,
  Button,
  ButtonGroup,
  Card,
  CardContent,
  Slider,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  PlayArrow as PlayIcon,
  Pause as PauseIcon,
  Refresh as RefreshIcon,
  Speed as SpeedIcon,
  Camera as CameraIcon,
  CheckCircle as PassIcon,
  Cancel as NgIcon,
  TrendingUp as TrendIcon,
} from '@mui/icons-material';
import Scene3D from '../components/3d/Scene3D';
import CameraView from '../components/CameraView';
import { useSimulatorStore } from '../store/simulatorStore';
import { api } from '../services/api';

const RoboticArmSimulator: React.FC = () => {
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  // Store狀態
  const {
    isRunning,
    isPaused,
    speed,
    stats,
    cameraView,
    threshold,
    workPieces,
    currentWorkPiece,
    armState,
    start,
    pause,
    resume,
    reset,
    setSpeed,
    setCameraView,
    setThreshold,
    addWorkPiece,
    updateWorkPiece,
    setCurrentWorkPiece,
    setArmState,
    setArmTarget,
    setGripperOpen,
    updateStats,
    updateElapsedTime,
  } = useSimulatorStore();

  // 模擬主控制邏輯
  useEffect(() => {
    if (isRunning && !isPaused) {
      // 開始模擬循環
      intervalRef.current = setInterval(() => {
        runSimulationCycle();
      }, 8000 / speed); // 基礎週期8秒，根據speed調整

      // 更新經過時間
      const timeInterval = setInterval(() => {
        updateElapsedTime();
      }, 1000);

      return () => {
        if (intervalRef.current) clearInterval(intervalRef.current);
        clearInterval(timeInterval);
      };
    }
  }, [isRunning, isPaused, speed]);

  // 模擬一個完整的分揀週期
  const runSimulationCycle = async () => {
    try {
      // 階段1: 生成新物件
      addWorkPiece();

      // 等待物件移動到檢測位置
      await sleep(2000 / speed);

      // 階段2: 檢測物件
      const pieces = useSimulatorStore.getState().workPieces;
      const pieceToDetect = pieces.find((p) => p.status === 'queue');

      if (!pieceToDetect) return;

      setCurrentWorkPiece(pieceToDetect);
      updateWorkPiece(pieceToDetect.id, {
        position: [2, 0.5, 0], // 移動到檢測位置
        status: 'detecting',
      });

      // 模擬檢測（隨機結果，實際應用中會呼叫API）
      await sleep(1000 / speed);
      const detectionResult = Math.random() > 0.3 ? 'PASS' : 'NG';

      updateWorkPiece(pieceToDetect.id, {
        detectionResult,
      });

      // 階段3: 手臂移動到物件
      setArmState('moving_to_object');
      setArmTarget([2, 1, 0]);
      await sleep(1500 / speed);

      // 階段4: 抓取物件
      setArmState('gripping');
      setGripperOpen(false);
      await sleep(500 / speed);

      updateWorkPiece(pieceToDetect.id, {
        status: 'gripped',
      });

      // 階段5: 移動到目標區域
      setArmState('moving_to_bin');
      const targetPosition: [number, number, number] =
        detectionResult === 'PASS' ? [-3, 1.5, -3] : [3, 1.5, -3];

      setArmTarget(targetPosition);
      await sleep(2000 / speed);

      // 階段6: 放置物件
      setArmState('releasing');
      setGripperOpen(true);

      const finalPosition: [number, number, number] =
        detectionResult === 'PASS' ? [-3, 0.5, -3] : [3, 0.5, -3];

      updateWorkPiece(pieceToDetect.id, {
        position: finalPosition,
        status: 'completed',
      });

      await sleep(500 / speed);

      // 階段7: 手臂回到初始位置
      setArmState('idle');
      setArmTarget(null);

      // 更新統計
      updateStats(detectionResult);

      // 清理完成的物件
      setTimeout(() => {
        const state = useSimulatorStore.getState();
        state.removeWorkPiece(pieceToDetect.id);
      }, 2000);

    } catch (error) {
      console.error('Simulation cycle error:', error);
    }
  };

  // 輔助函數：延遲
  const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

  // 格式化時間顯示
  const formatTime = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes
      .toString()
      .padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <Container maxWidth="xl" sx={{ py: 3 }}>
      {/* 標題 */}
      <Typography variant="h4" gutterBottom>
        🤖 3D機械手臂智能分揀模擬器
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        Robotic Arm Sorting Simulator with AI Detection
      </Typography>

      <Grid container spacing={3} sx={{ mt: 1 }}>
        {/* 左側：3D場景和相機視角 */}
        <Grid item xs={12} lg={8}>
          {/* 3D場景 */}
          <Paper sx={{ p: 2, mb: 2 }}>
            <Typography variant="h6" gutterBottom>
              3D模擬場景
            </Typography>
            <Scene3D />

            {/* 控制按鈕 */}
            <Box sx={{ mt: 2, display: 'flex', gap: 2, alignItems: 'center' }}>
              <ButtonGroup variant="contained" size="large">
                <Button
                  startIcon={<PlayIcon />}
                  onClick={isRunning && !isPaused ? pause : isRunning ? resume : start}
                  color={isRunning && !isPaused ? 'warning' : 'primary'}
                >
                  {isRunning && !isPaused ? '暫停' : isRunning ? '繼續' : '開始'}
                </Button>
                <Button startIcon={<RefreshIcon />} onClick={reset} color="error">
                  重置
                </Button>
              </ButtonGroup>

              {/* 狀態指示 */}
              {isRunning && (
                <Chip
                  label={isPaused ? '已暫停' : '運行中'}
                  color={isPaused ? 'default' : 'success'}
                  icon={isPaused ? <PauseIcon /> : <PlayIcon />}
                />
              )}

              {/* 手臂狀態 */}
              <Chip
                label={`手臂: ${armState}`}
                size="small"
                variant="outlined"
              />

              {/* 物件數量 */}
              <Chip
                label={`物件: ${workPieces.length}`}
                size="small"
                variant="outlined"
              />
            </Box>
          </Paper>

          {/* 手臂相機視角 */}
          <Box sx={{ mt: 2 }}>
            <CameraView />
          </Box>

          {/* 參數控制 */}
          <Paper sx={{ p: 2, mt: 2 }}>
            <Typography variant="h6" gutterBottom>
              控制參數
            </Typography>

            <Grid container spacing={3}>
              <Grid item xs={12} sm={4}>
                <Box>
                  <Typography gutterBottom>
                    <SpeedIcon fontSize="small" /> 模擬速度: {speed.toFixed(1)}x
                  </Typography>
                  <Slider
                    value={speed}
                    onChange={(e, v) => setSpeed(v as number)}
                    min={0.5}
                    max={3}
                    step={0.1}
                    marks={[
                      { value: 0.5, label: '0.5x' },
                      { value: 1, label: '1x' },
                      { value: 2, label: '2x' },
                      { value: 3, label: '3x' },
                    ]}
                    disabled={isRunning}
                  />
                </Box>
              </Grid>

              <Grid item xs={12} sm={4}>
                <FormControl fullWidth size="small">
                  <InputLabel>
                    <CameraIcon fontSize="small" /> 相機視角
                  </InputLabel>
                  <Select
                    value={cameraView}
                    label="相機視角"
                    onChange={(e) => setCameraView(e.target.value as any)}
                  >
                    <MenuItem value="free">自由視角</MenuItem>
                    <MenuItem value="top">俯視圖</MenuItem>
                    <MenuItem value="side">側視圖</MenuItem>
                    <MenuItem value="front">正視圖</MenuItem>
                  </Select>
                </FormControl>
              </Grid>

              <Grid item xs={12} sm={4}>
                <Typography gutterBottom>檢測閾值: {threshold}</Typography>
                <Slider
                  value={threshold}
                  onChange={(e, v) => setThreshold(v as number)}
                  min={10}
                  max={100}
                  step={5}
                  disabled={isRunning}
                />
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* 右側：統計面板 */}
        <Grid item xs={12} lg={4}>
          {/* 統計卡片 */}
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    總處理數
                  </Typography>
                  <Typography variant="h3">{stats.totalProcessed}</Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={6}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    良率
                  </Typography>
                  <Typography variant="h3" color="success.main">
                    {stats.yieldRate.toFixed(1)}%
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={6}>
              <Card sx={{ bgcolor: '#e8f5e9' }}>
                <CardContent>
                  <PassIcon color="success" />
                  <Typography color="text.secondary">正確 (PASS)</Typography>
                  <Typography variant="h4" color="success.main">
                    {stats.passCount}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={6}>
              <Card sx={{ bgcolor: '#ffebee' }}>
                <CardContent>
                  <NgIcon color="error" />
                  <Typography color="text.secondary">錯誤 (NG)</Typography>
                  <Typography variant="h4" color="error.main">
                    {stats.ngCount}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography color="text.secondary" gutterBottom>
                    <TrendIcon fontSize="small" /> 處理速度
                  </Typography>
                  <Typography variant="h5">
                    {stats.currentSpeed.toFixed(1)} 件/小時
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    運行時間: {formatTime(stats.elapsedTime)}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>

            {/* 進度條 */}
            {isRunning && !isPaused && (
              <Grid item xs={12}>
                <Card>
                  <CardContent>
                    <Typography gutterBottom>處理中...</Typography>
                    <LinearProgress />
                  </CardContent>
                </Card>
              </Grid>
            )}
          </Grid>

          {/* 說明文字 */}
          <Paper sx={{ p: 2, mt: 2 }}>
            <Typography variant="h6" gutterBottom>
              操作說明
            </Typography>
            <Typography variant="body2" paragraph>
              1. 點擊「開始」按鈕啟動自動分揀模擬
            </Typography>
            <Typography variant="body2" paragraph>
              2. 物件將自動出現在傳送帶上
            </Typography>
            <Typography variant="body2" paragraph>
              3. 機械手臂會自動拍照、檢測、分揀
            </Typography>
            <Typography variant="body2" paragraph>
              4. 正確的物件放入綠色區域，錯誤的放入紅色區域
            </Typography>
            <Typography variant="body2">
              5. 調整速度可以加快或減慢模擬過程
            </Typography>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default RoboticArmSimulator;
