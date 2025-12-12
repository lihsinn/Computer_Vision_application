/**
 * Main App Component
 * 應用程式主要入口
 */

import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

// Layout
import Layout from './components/Layout';

// Pages
import HomePage from './pages/HomePage';
import SingleInspectionPage from './pages/SingleInspectionPage';
import RoboticArmSimulator from './pages/RoboticArmSimulator';

// Create MUI theme
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<HomePage />} />
            <Route path="single-inspection" element={<SingleInspectionPage />} />
            <Route path="robotic-arm-simulator" element={<RoboticArmSimulator />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;
