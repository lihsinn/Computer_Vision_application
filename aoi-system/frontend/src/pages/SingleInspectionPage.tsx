/**
 * Single Inspection Page - 單片檢測頁面
 * 主題1: 單片檢測自動儲存瑕疵工單
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Button,
  TextField,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Alert,
  CircularProgress,
  Divider,
  SelectChangeEvent,
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  PlayArrow as RunIcon,
  Save as SaveIcon,
  Add as AddIcon,
} from '@mui/icons-material';
import { api } from '../services/api';

interface InspectionResult {
  id: string;
  serial_number: string;
  side: 'A' | 'B';
  judgment_result: 'PASS' | 'NG';
  yield_rate: number;
  ng_count: number;
  total_cells: number;
  positioning_abnormal: boolean;
  running_result: string;
  created_at: string;
}

const SingleInspectionPage: React.FC = () => {
  // State management
  const [inspectionMode, setInspectionMode] = useState<'Run' | 'OfflineTest'>('OfflineTest');
  const [lots, setLots] = useState<any[]>([]);
  const [selectedLotId, setSelectedLotId] = useState<string>('');
  const [newLotNumber, setNewLotNumber] = useState<string>('');
  const [serialNumber, setSerialNumber] = useState<string>('001');
  const [side, setSide] = useState<'A' | 'B'>('A');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [threshold, setThreshold] = useState<number>(30);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [inspectionResults, setInspectionResults] = useState<InspectionResult[]>([]);
  const [error, setError] = useState<string>('');
  const [success, setSuccess] = useState<string>('');

  // Load lots on component mount
  useEffect(() => {
    loadLots();
  }, []);

  const loadLots = async () => {
    try {
      const response = await api.getLots();
      setLots(response.lots || []);
    } catch (err) {
      console.error('Failed to load lots:', err);
      setError('無法載入批次列表');
    }
  };

  const handleCreateLot = async () => {
    if (!newLotNumber.trim()) {
      setError('請輸入批號');
      return;
    }

    try {
      const response = await api.createLot(newLotNumber, '單片檢測批次');
      setSuccess(`批次 ${newLotNumber} 建立成功！`);
      setNewLotNumber('');
      await loadLots();
      setSelectedLotId(response.lot.id);
    } catch (err: any) {
      setError(err.response?.data?.error || '建立批次失敗');
    }
  };

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setSelectedFile(event.target.files[0]);
      setError('');
    }
  };

  const handleRunInspection = async () => {
    // Validation
    if (!selectedLotId) {
      setError('請選擇批次');
      return;
    }

    if (!selectedFile) {
      setError('請選擇檢測影像');
      return;
    }

    if (!serialNumber.trim()) {
      setError('請輸入序號');
      return;
    }

    setIsProcessing(true);
    setError('');
    setSuccess('');

    try {
      // Step 1: Upload image
      const uploadResult = await api.uploadImage(selectedFile);
      console.log('Image uploaded:', uploadResult);

      // Step 2: Run defect detection
      const detectionResult = await api.detectDefects(uploadResult.image_id, threshold);
      console.log('Detection result:', detectionResult);

      // Step 3: Prepare cells and defects data
      const cells = detectionResult.defects.map((defect: any, index: number) => ({
        cell_number: index + 1,
        position_x: defect.x,
        position_y: defect.y,
        width: defect.width || 50,
        height: defect.height || 50,
        status: 'NG', // All detected defects are NG
      }));

      // Add PASS cells (simplified - in real scenario, you'd have grid detection)
      const totalCells = 100; // Example: 10x10 grid
      const passCells = [];
      for (let i = cells.length; i < totalCells; i++) {
        passCells.push({
          cell_number: i + 1,
          position_x: (i % 10) * 100,
          position_y: Math.floor(i / 10) * 100,
          width: 50,
          height: 50,
          status: 'PASS',
        });
      }

      const allCells = [...cells, ...passCells];

      // Prepare defects by cell
      const defectsByCell: any = {};
      detectionResult.defects.forEach((defect: any, index: number) => {
        defectsByCell[index + 1] = [
          {
            defect_type: 'UNKNOWN',
            position_x: defect.x,
            position_y: defect.y,
            area: defect.area,
            width: defect.width,
            height: defect.height,
          },
        ];
      });

      // Step 4: Save inspection record
      const inspectionData = {
        lot_id: selectedLotId,
        serial_number: serialNumber,
        side: side,
        inspection_mode: inspectionMode,
        inspection_type: 'SingleInsp' as const,
        image_path: uploadResult.filename,
        annotated_image_path: detectionResult.annotated_image ? 'annotated.jpg' : undefined,
        cells: allCells,
        defects: defectsByCell,
        threshold: threshold,
        running_result: 'SUCCESS',
        positioning_abnormal: false,
      };

      const saveResult = await api.createInspection(inspectionData);
      console.log('Inspection saved:', saveResult);

      // Step 5: Reload inspection results
      await loadInspectionResults();

      setSuccess(`檢測完成！序號: ${serialNumber}, 判定結果: ${saveResult.inspection.judgment_result}`);
      setSelectedFile(null);
      setSerialNumber((parseInt(serialNumber) + 1).toString().padStart(3, '0'));
    } catch (err: any) {
      console.error('Inspection failed:', err);
      setError(err.response?.data?.error || '檢測失敗');
    } finally {
      setIsProcessing(false);
    }
  };

  const loadInspectionResults = async () => {
    if (!selectedLotId) return;

    try {
      const response = await api.getInspections({ lot_id: selectedLotId });
      setInspectionResults(response.inspections || []);
    } catch (err) {
      console.error('Failed to load inspection results:', err);
    }
  };

  useEffect(() => {
    if (selectedLotId) {
      loadInspectionResults();
    }
  }, [selectedLotId]);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        單片檢測 - Single Chip Inspection
      </Typography>
      <Typography variant="subtitle1" color="text.secondary" gutterBottom>
        主題1: 單片檢測自動儲存瑕疵工單
      </Typography>

      {/* Alerts */}
      {error && (
        <Alert severity="error" onClose={() => setError('')} sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      {success && (
        <Alert severity="success" onClose={() => setSuccess('')} sx={{ mb: 2 }}>
          {success}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Left Panel - Configuration */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              檢測設定
            </Typography>

            {/* Inspection Mode */}
            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>檢測模式</InputLabel>
              <Select
                value={inspectionMode}
                label="檢測模式"
                onChange={(e: SelectChangeEvent<'Run' | 'OfflineTest'>) =>
                  setInspectionMode(e.target.value as 'Run' | 'OfflineTest')
                }
              >
                <MenuItem value="OfflineTest">離線檢測 (OffLine Test)</MenuItem>
                <MenuItem value="Run">執行模式 (Run)</MenuItem>
              </Select>
            </FormControl>

            <Divider sx={{ my: 2 }} />

            {/* Lot Selection */}
            <Typography variant="subtitle2" gutterBottom>
              批次管理
            </Typography>

            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>選擇批次 (LotNum)</InputLabel>
              <Select
                value={selectedLotId}
                label="選擇批次 (LotNum)"
                onChange={(e: SelectChangeEvent) => setSelectedLotId(e.target.value)}
              >
                {lots.map((lot) => (
                  <MenuItem key={lot.id} value={lot.id}>
                    {lot.lot_number} ({lot.status})
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            {/* Create New Lot */}
            <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
              <TextField
                size="small"
                label="新批號"
                value={newLotNumber}
                onChange={(e) => setNewLotNumber(e.target.value)}
                placeholder="LOT001"
                fullWidth
              />
              <Button
                variant="outlined"
                startIcon={<AddIcon />}
                onClick={handleCreateLot}
                disabled={!newLotNumber.trim()}
              >
                建立
              </Button>
            </Box>

            <Divider sx={{ my: 2 }} />

            {/* Serial Number and Side */}
            <TextField
              fullWidth
              label="序號 (Serial Number)"
              value={serialNumber}
              onChange={(e) => setSerialNumber(e.target.value)}
              sx={{ mb: 2 }}
            />

            <FormControl fullWidth sx={{ mb: 2 }}>
              <InputLabel>面別 (Side)</InputLabel>
              <Select
                value={side}
                label="面別 (Side)"
                onChange={(e: SelectChangeEvent<'A' | 'B'>) =>
                  setSide(e.target.value as 'A' | 'B')
                }
              >
                <MenuItem value="A">A面</MenuItem>
                <MenuItem value="B">B面</MenuItem>
              </Select>
            </FormControl>

            {/* Threshold */}
            <TextField
              fullWidth
              type="number"
              label="檢測閾值 (Threshold)"
              value={threshold}
              onChange={(e) => setThreshold(parseInt(e.target.value))}
              inputProps={{ min: 10, max: 100 }}
              sx={{ mb: 2 }}
            />

            {/* File Upload */}
            <Button
              variant="outlined"
              component="label"
              startIcon={<UploadIcon />}
              fullWidth
              sx={{ mb: 2 }}
            >
              選擇影像
              <input type="file" hidden accept="image/*" onChange={handleFileSelect} />
            </Button>

            {selectedFile && (
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                已選擇: {selectedFile.name}
              </Typography>
            )}

            {/* Run Inspection Button */}
            <Button
              variant="contained"
              size="large"
              fullWidth
              startIcon={isProcessing ? <CircularProgress size={20} /> : <RunIcon />}
              onClick={handleRunInspection}
              disabled={isProcessing || !selectedLotId || !selectedFile}
            >
              {isProcessing ? '檢測中...' : '執行檢測'}
            </Button>
          </Paper>
        </Grid>

        {/* Right Panel - Results */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              檢測結果
            </Typography>

            {inspectionResults.length === 0 ? (
              <Box
                sx={{
                  display: 'flex',
                  justifyContent: 'center',
                  alignItems: 'center',
                  minHeight: 300,
                }}
              >
                <Typography color="text.secondary">尚無檢測記錄</Typography>
              </Box>
            ) : (
              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>序號</TableCell>
                      <TableCell>面別</TableCell>
                      <TableCell>運行結果</TableCell>
                      <TableCell>判定結果</TableCell>
                      <TableCell>良率 (%)</TableCell>
                      <TableCell>NG顆數</TableCell>
                      <TableCell>總Cell數</TableCell>
                      <TableCell>定位異常</TableCell>
                      <TableCell>檢測時間</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {inspectionResults.map((result) => (
                      <TableRow key={result.id}>
                        <TableCell>{result.serial_number}</TableCell>
                        <TableCell>
                          <Chip label={result.side} size="small" />
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={result.running_result}
                            size="small"
                            color={result.running_result === 'SUCCESS' ? 'success' : 'error'}
                          />
                        </TableCell>
                        <TableCell>
                          <Chip
                            label={result.judgment_result}
                            size="small"
                            color={result.judgment_result === 'PASS' ? 'success' : 'error'}
                          />
                        </TableCell>
                        <TableCell>{result.yield_rate.toFixed(2)}%</TableCell>
                        <TableCell>{result.ng_count}</TableCell>
                        <TableCell>{result.total_cells}</TableCell>
                        <TableCell>
                          {result.positioning_abnormal ? (
                            <Chip label="異常" size="small" color="warning" />
                          ) : (
                            <Chip label="正常" size="small" color="default" />
                          )}
                        </TableCell>
                        <TableCell>
                          {new Date(result.created_at).toLocaleString('zh-TW')}
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </Paper>

          {/* Statistics Summary */}
          {inspectionResults.length > 0 && (
            <Grid container spacing={2} sx={{ mt: 2 }}>
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      總檢測數
                    </Typography>
                    <Typography variant="h4">{inspectionResults.length}</Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      平均良率
                    </Typography>
                    <Typography variant="h4" color="success.main">
                      {(
                        inspectionResults.reduce((sum, r) => sum + parseFloat(r.yield_rate.toString()), 0) /
                        inspectionResults.length
                      ).toFixed(2)}
                      %
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      總NG數
                    </Typography>
                    <Typography variant="h4" color="error.main">
                      {inspectionResults.reduce((sum, r) => sum + r.ng_count, 0)}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Card>
                  <CardContent>
                    <Typography color="text.secondary" gutterBottom>
                      定位異常數
                    </Typography>
                    <Typography variant="h4" color="warning.main">
                      {inspectionResults.filter((r) => r.positioning_abnormal).length}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          )}
        </Grid>
      </Grid>
    </Box>
  );
};

export default SingleInspectionPage;
