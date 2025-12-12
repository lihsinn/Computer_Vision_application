import React, { useState } from 'react';
import {
  Box,
  Typography,
  Tabs,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip
} from '@mui/material';
import {
  BugReport,
  Straighten,
  GpsFixed,
  CheckCircle
} from '@mui/icons-material';
import { Defect, Measurement, FiducialMark } from '../types/aoi.types';

interface ResultsPanelProps {
  defects?: Defect[];
  measurements?: Measurement[];
  marks?: FiducialMark[];
  rotationAngle?: number | null;
}

const ResultsPanel: React.FC<ResultsPanelProps> = ({
  defects,
  measurements,
  marks,
  rotationAngle
}) => {
  const [activeTab, setActiveTab] = useState(0);

  const hasDefects = defects && defects.length > 0;
  const hasMeasurements = measurements && measurements.length > 0;
  const hasMarks = marks && marks.length > 0;
  const hasAnyResults = hasDefects || hasMeasurements || hasMarks;

  if (!hasAnyResults) {
    return (
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: 300,
          p: 4
        }}
      >
        <CheckCircle sx={{ fontSize: 64, color: 'success.light', mb: 2 }} />
        <Typography variant="h6" gutterBottom>
          尚無結果
        </Typography>
        <Typography variant="body2" color="text.secondary">
          上傳圖像並運行處理以查看結果
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={activeTab} onChange={(_, v) => setActiveTab(v)}>
          {hasDefects && (
            <Tab
              icon={<BugReport />}
              label={`瑕疵 (${defects.length})`}
              iconPosition="start"
            />
          )}
          {hasMeasurements && (
            <Tab
              icon={<Straighten />}
              label={`測量 (${measurements.length})`}
              iconPosition="start"
            />
          )}
          {hasMarks && (
            <Tab
              icon={<GpsFixed />}
              label={`標記 (${marks.length})`}
              iconPosition="start"
            />
          )}
        </Tabs>
      </Box>

      <Box sx={{ p: 2 }}>
        {activeTab === 0 && hasDefects && (
          <Box>
            <Box sx={{ mb: 2, p: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
              <Typography variant="subtitle1">
                <strong>總瑕疵數:</strong> {defects.length}
              </Typography>
            </Box>
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow sx={{ bgcolor: '#fafafa' }}>
                    <TableCell><strong>ID</strong></TableCell>
                    <TableCell><strong>位置 (x, y)</strong></TableCell>
                    <TableCell><strong>面積 (px²)</strong></TableCell>
                    <TableCell><strong>尺寸 (w × h)</strong></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {defects.map((defect) => (
                    <TableRow key={defect.id} hover>
                      <TableCell>
                        <Chip label={`D${defect.id}`} size="small" color="error" />
                      </TableCell>
                      <TableCell>
                        ({defect.position.x}, {defect.position.y})
                      </TableCell>
                      <TableCell>{defect.area.toFixed(0)}</TableCell>
                      <TableCell>
                        {defect.bbox.width} × {defect.bbox.height}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        )}

        {activeTab === 1 && hasMeasurements && (
          <Box>
            <Box sx={{ mb: 2, p: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
              <Typography variant="subtitle1">
                <strong>總物體數:</strong> {measurements.length}
              </Typography>
            </Box>
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow sx={{ bgcolor: '#fafafa' }}>
                    <TableCell><strong>ID</strong></TableCell>
                    <TableCell><strong>形狀</strong></TableCell>
                    <TableCell><strong>寬度 (mm)</strong></TableCell>
                    <TableCell><strong>高度 (mm)</strong></TableCell>
                    <TableCell><strong>面積 (mm²)</strong></TableCell>
                    <TableCell><strong>直徑 (mm)</strong></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {measurements.map((m) => (
                    <TableRow key={m.object_id} hover>
                      <TableCell>{m.object_id}</TableCell>
                      <TableCell>
                        <Chip
                          label={m.shape === 'circle' ? '● 圓形' : '▭ 矩形'}
                          size="small"
                          color={m.shape === 'circle' ? 'primary' : 'warning'}
                        />
                      </TableCell>
                      <TableCell>{m.width_mm}</TableCell>
                      <TableCell>{m.height_mm}</TableCell>
                      <TableCell>{m.area_mm2}</TableCell>
                      <TableCell>{m.diameter_mm || '-'}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        )}

        {activeTab === 2 && hasMarks && (
          <Box>
            <Box sx={{ mb: 2, p: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
              <Typography variant="subtitle1">
                <strong>總標記數:</strong> {marks.length}
                {rotationAngle !== null && rotationAngle !== undefined && (
                  <span style={{ marginLeft: 16 }}>
                    | <strong>旋轉角度:</strong> {rotationAngle.toFixed(2)}°
                  </span>
                )}
              </Typography>
            </Box>
            <TableContainer component={Paper} variant="outlined">
              <Table size="small">
                <TableHead>
                  <TableRow sx={{ bgcolor: '#fafafa' }}>
                    <TableCell><strong>標記 ID</strong></TableCell>
                    <TableCell><strong>位置 (x, y)</strong></TableCell>
                    <TableCell><strong>半徑 (px)</strong></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {marks.map((mark) => (
                    <TableRow key={mark.id} hover>
                      <TableCell>
                        <Chip label={`M${mark.id}`} size="small" color="success" />
                      </TableCell>
                      <TableCell>
                        ({mark.position.x}, {mark.position.y})
                      </TableCell>
                      <TableCell>{mark.radius}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Box>
        )}
      </Box>
    </Box>
  );
};

export default ResultsPanel;
