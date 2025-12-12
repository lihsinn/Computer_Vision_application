/**
 * Main Layout Component
 * 應用程式主要布局，包含導航側邊欄
 */

import React, { useState } from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  List,
  Typography,
  Divider,
  IconButton,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Home as HomeIcon,
  Science as ScienceIcon,
  SmartToy as SmartToyIcon,
  Assessment as AssessmentIcon,
} from '@mui/icons-material';

const drawerWidth = 240;

interface MenuItem {
  text: string;
  icon: React.ReactElement;
  path: string;
}

const menuItems: MenuItem[] = [
  {
    text: '首頁',
    icon: <HomeIcon />,
    path: '/',
  },
  {
    text: '單片檢測',
    icon: <ScienceIcon />,
    path: '/single-inspection',
  },
  {
    text: '機械手臂模擬器',
    icon: <SmartToyIcon />,
    path: '/robotic-arm-simulator',
  },
];

const Layout: React.FC = () => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const location = useLocation();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const drawer = (
    <Box>
      <Toolbar>
        <Typography variant="h6" noWrap component="div">
          AOI 系統
        </Typography>
      </Toolbar>
      <Divider />
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              component={Link}
              to={item.path}
              selected={location.pathname === item.path}
              onClick={() => setMobileOpen(false)}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <Box sx={{ display: 'flex' }}>
      {/* App Bar */}
      <AppBar
        position="fixed"
        sx={{
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          ml: { sm: `${drawerWidth}px` },
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { sm: 'none' } }}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" noWrap component="div">
            自動光學檢測系統
          </Typography>
        </Toolbar>
      </AppBar>

      {/* Mobile Drawer */}
      <Box
        component="nav"
        sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      >
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
          sx={{
            display: { xs: 'block', sm: 'none' },
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
            },
          }}
        >
          {drawer}
        </Drawer>

        {/* Desktop Drawer */}
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', sm: 'block' },
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
            },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      {/* Main Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { sm: `calc(100% - ${drawerWidth}px)` },
          minHeight: '100vh',
          bgcolor: '#f5f5f5',
        }}
      >
        <Toolbar />
        <Outlet />
      </Box>
    </Box>
  );
};

export default Layout;
