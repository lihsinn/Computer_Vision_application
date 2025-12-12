import React, { useState } from 'react';
import {
  Box,
  Container,
  Paper,
  Typography,
  AppBar,
  Toolbar,
  Grid,
  Button,
  ButtonGroup,
  Slider,
  TextField,
  Alert,
  CircularProgress,
  Chip
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  BugReport as DefectIcon,
  Straighten as MeasureIcon,
  GpsFixed as FiducialIcon,
  PlayArrow as PlayIcon,
  Refresh as ResetIcon
} from '@mui/icons-material';
import ImageUpload from './components/ImageUpload';
import ImageViewer from './components/ImageViewer';
import ResultsPanel from './components/ResultsPanel';
import { api } from './services/api';
import {
  UploadResponse,
  Defect,
  Measurement,
  FiducialMark,
  ProcessingMode
} from './types/aoi.types';

function App() {
  const [uploadResponse, setUploadResponse] = useState<UploadResponse | null>(null);
  const [annotatedImage, setAnnotatedImage] = useState<string | null>(null);
  const [defects, setDefects] = useState<Defect[]>([]);
  const [measurements, setMeasurements] = useState<Measurement[]>([]);
  const [marks, setMarks] = useState<FiducialMark[]>([]);
  const [rotationAngle, setRotationAngle] = useState<number | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [processingMode, setProcessingMode] = useState<ProcessingMode>('defect');
  const [threshold, setThreshold] = useState(30);
  const [calibration, setCalibration] = useState(0.1);
  const [minRadius, setMinRadius] = useState(5);
  const [maxRadius, setMaxRadius] = useState(25);

  const handleUploadSuccess = (response: UploadResponse) => {
    setUploadResponse(response);
    setAnnotatedImage(null);
    setDefects([]);
    setMeasurements([]);
    setMarks([]);
    setRotationAngle(null);
    setError(null);
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
    setTimeout(() => setError(null), 5000);
  };

  const handleProcess = async () => {
    if (!uploadResponse) {
      handleError('請先上傳圖像');
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      if (processingMode === 'defect') {
        const result = await api.detectDefects(uploadResponse.image_id, threshold);
        setDefects(result.defects);
        setAnnotatedImage(result.annotated_image);
      } else if (processingMode === 'measurement') {
        const result = await api.measureDimensions(uploadResponse.image_id, calibration);
        setMeasurements(result.measurements);
        setAnnotatedImage(result.annotated_image);
      } else if (processingMode === 'fiducial') {
        const result = await api.detectFiducialMarks(uploadResponse.image_id, minRadius, maxRadius);
        setMarks(result.marks);
        setRotationAngle(result.rotation_angle);
        setAnnotatedImage(result.annotated_image);
      }
    } catch (error: any) {
      const errorMessage = error.response?.data?.error?.message || '處理失敗';
      handleError(errorMessage);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleReset = () => {
    setUploadResponse(null);
    setAnnotatedImage(null);
    setDefects([]);
    setMeasurements([]);
    setMarks([]);
    setRotationAngle(null);
    setError(null);
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh', bgcolor: '#f5f5f5' }}>
      <AppBar position="static" sx={{ background: '#667eea' }}>
        <Toolbar>
          {/* <BugReport sx={{ mr: 2 }} /> */}
          <Typography variant="h5" component="div" sx={{ flexGrow: 1, fontWeight: 600 }}>
            AOI 檢測系統
          </Typography>
          <Typography variant="body2" sx={{ opacity: 0.9 }}>
            自動光學檢測 - 缺陷檢測與測量
          </Typography>
        </Toolbar>
      </AppBar>

      {error && (
        <Alert severity="error" onClose={() => setError(null)} sx={{ m: 2 }}>
          {error}
        </Alert>
      )}

      <Container maxWidth="xl" sx={{ mt: 3, mb: 3, flex: 1 }}>
        <Grid container spacing={3}>
          {/* 左側控制面板 */}
          <Grid item xs={12} md={4}>
            <Paper sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <UploadIcon /> 1. 上傳圖像
              </Typography>
              <ImageUpload onUploadSuccess={handleUploadSuccess} onError={handleError} />
              {uploadResponse && (
                <Box sx={{ mt: 2, p: 2, bgcolor: '#e8f5e9', borderRadius: 1 }}>
                  <Typography variant="body2" color="success.dark">
                    ✓ {uploadResponse.filename}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    尺寸: {uploadResponse.size.width} × {uploadResponse.size.height} px
                  </Typography>
                </Box>
              )}
            </Paper>

            <Paper sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                2. 選擇處理模式
              </Typography>
              <ButtonGroup fullWidth variant="outlined" sx={{ mb: 2 }}>
                <Button
                  variant={processingMode === 'defect' ? 'contained' : 'outlined'}
                  onClick={() => setProcessingMode('defect')}
                  startIcon={<DefectIcon />}
                >
                  瑕疵檢測
                </Button>
                <Button
                  variant={processingMode === 'measurement' ? 'contained' : 'outlined'}
                  onClick={() => setProcessingMode('measurement')}
                  startIcon={<MeasureIcon />}
                >
                  尺寸測量
                </Button>
                <Button
                  variant={processingMode === 'fiducial' ? 'contained' : 'outlined'}
                  onClick={() => setProcessingMode('fiducial')}
                  startIcon={<FiducialIcon />}
                >
                  定位標記
                </Button>
              </ButtonGroup>

              <Typography variant="subtitle2" gutterBottom sx={{ mt: 3 }}>
                參數設置
              </Typography>

              {processingMode === 'defect' && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="body2" gutterBottom>
                    閾值: {threshold}
                  </Typography>
                  <Slider
                    value={threshold}
                    onChange={(_, val) => setThreshold(val as number)}
                    min={10}
                    max={100}
                    valueLabelDisplay="auto"
                  />
                </Box>
              )}

              {processingMode === 'measurement' && (
                <TextField
                  fullWidth
                  label="校準係數 (mm/pixel)"
                  type="number"
                  value={calibration}
                  onChange={(e) => setCalibration(Number(e.target.value))}
                  inputProps={{ step: 0.01, min: 0.01, max: 1 }}
                  sx={{ mt: 2 }}
                />
              )}

              {processingMode === 'fiducial' && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="body2" gutterBottom>
                    最小半徑: {minRadius}
                  </Typography>
                  <Slider
                    value={minRadius}
                    onChange={(_, val) => setMinRadius(val as number)}
                    min={1}
                    max={50}
                    valueLabelDisplay="auto"
                  />
                  <Typography variant="body2" gutterBottom sx={{ mt: 2 }}>
                    最大半徑: {maxRadius}
                  </Typography>
                  <Slider
                    value={maxRadius}
                    onChange={(_, val) => setMaxRadius(val as number)}
                    min={10}
                    max={100}
                    valueLabelDisplay="auto"
                  />
                </Box>
              )}

              <Box sx={{ mt: 3, display: 'flex', gap: 1 }}>
                <Button
                  fullWidth
                  variant="contained"
                  color="success"
                  size="large"
                  startIcon={isProcessing ? <CircularProgress size={20} color="inherit" /> : <PlayIcon />}
                  onClick={handleProcess}
                  disabled={!uploadResponse || isProcessing}
                >
                  {isProcessing ? '處理中...' : '開始處理'}
                </Button>
                <Button
                  variant="outlined"
                  color="error"
                  startIcon={<ResetIcon />}
                  onClick={handleReset}
                  disabled={isProcessing}
                >
                  重置
                </Button>
              </Box>
            </Paper>
          </Grid>

          {/* 右側結果面板 */}
          <Grid item xs={12} md={8}>
            <Paper sx={{ p: 0, mb: 3, minHeight: 500 }}>
              <ImageViewer annotatedImage={annotatedImage} />
            </Paper>

            <Paper sx={{ p: 0 }}>
              <ResultsPanel
                defects={defects}
                measurements={measurements}
                marks={marks}
                rotationAngle={rotationAngle}
              />
            </Paper>
          </Grid>
        </Grid>
      </Container>

    </Box>
  );
}

export default App;
