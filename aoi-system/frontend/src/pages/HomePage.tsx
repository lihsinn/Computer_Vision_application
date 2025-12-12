/**
 * Home Page Component
 * 系統首頁
 */

import React from 'react';
import { Link } from 'react-router-dom';
import {
  Box,
  Container,
  Grid,
  Card,
  CardContent,
  CardActions,
  Typography,
  Button,
  Paper,
} from '@mui/material';
import {
  Science as ScienceIcon,
  SmartToy as SmartToyIcon,
  Assessment as AssessmentIcon,
  CheckCircle as CheckCircleIcon,
} from '@mui/icons-material';

const HomePage: React.FC = () => {
  const features = [
    {
      title: '單片檢測',
      description: '執行單片AOI檢測，支援離線檢測和實時執行模式，自動儲存檢測記錄到資料庫',
      icon: <ScienceIcon sx={{ fontSize: 60, color: '#1976d2' }} />,
      link: '/single-inspection',
      status: '已完成',
    },
    {
      title: '機械手臂模擬器',
      description: 'UR機械手臂3D視覺化模擬器，展示自動分揀流程，包含6自由度機械手臂控制',
      icon: <SmartToyIcon sx={{ fontSize: 60, color: '#2e7d32' }} />,
      link: '/robotic-arm-simulator',
      status: '已完成',
    },
  ];

  return (
    <Container maxWidth="lg">
      {/* Header */}
      <Paper
        elevation={3}
        sx={{
          p: 4,
          mb: 4,
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
        }}
      >
        <Typography variant="h3" gutterBottom fontWeight="bold">
          AOI 自動光學檢測系統
        </Typography>
        <Typography variant="h6">
          Automated Optical Inspection System
        </Typography>
        <Typography variant="body1" sx={{ mt: 2, opacity: 0.9 }}>
          先進的視覺檢測解決方案，結合AI技術與3D視覺化，提供高效、精準的品質檢測服務
        </Typography>
      </Paper>

      {/* System Status */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h5" gutterBottom fontWeight="bold">
          系統狀態
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={4}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <CheckCircleIcon sx={{ fontSize: 40, color: '#2e7d32' }} />
              <Typography variant="h6">後端服務</Typography>
              <Typography variant="body2" color="success.main">
                運行中
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <CheckCircleIcon sx={{ fontSize: 40, color: '#2e7d32' }} />
              <Typography variant="h6">資料庫</Typography>
              <Typography variant="body2" color="success.main">
                已連接
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <CheckCircleIcon sx={{ fontSize: 40, color: '#2e7d32' }} />
              <Typography variant="h6">3D渲染</Typography>
              <Typography variant="body2" color="success.main">
                正常
              </Typography>
            </Paper>
          </Grid>
        </Grid>
      </Box>

      {/* Feature Cards */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h5" gutterBottom fontWeight="bold">
          功能模組
        </Typography>
        <Grid container spacing={3}>
          {features.map((feature, index) => (
            <Grid item xs={12} md={6} key={index}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  transition: 'transform 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: 6,
                  },
                }}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    {feature.icon}
                    <Box sx={{ ml: 2 }}>
                      <Typography variant="h5" component="div">
                        {feature.title}
                      </Typography>
                      <Typography variant="caption" color="success.main">
                        {feature.status}
                      </Typography>
                    </Box>
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    {feature.description}
                  </Typography>
                </CardContent>
                <CardActions>
                  <Button
                    component={Link}
                    to={feature.link}
                    size="large"
                    variant="contained"
                    fullWidth
                  >
                    開啟功能
                  </Button>
                </CardActions>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* System Info */}
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          系統資訊
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2" color="text.secondary">
              <strong>前端框架：</strong> React + TypeScript + Material-UI
            </Typography>
            <Typography variant="body2" color="text.secondary">
              <strong>3D引擎：</strong> Three.js + React Three Fiber
            </Typography>
            <Typography variant="body2" color="text.secondary">
              <strong>狀態管理：</strong> Zustand
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="body2" color="text.secondary">
              <strong>後端框架：</strong> Flask + SQLAlchemy
            </Typography>
            <Typography variant="body2" color="text.secondary">
              <strong>資料庫：</strong> PostgreSQL
            </Typography>
            <Typography variant="body2" color="text.secondary">
              <strong>版本：</strong> 1.0.0
            </Typography>
          </Grid>
        </Grid>
      </Paper>
    </Container>
  );
};

export default HomePage;
