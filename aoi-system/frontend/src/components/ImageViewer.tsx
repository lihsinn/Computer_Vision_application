import React from 'react';
import { Box, Typography } from '@mui/material';
import { Image as ImageIcon } from '@mui/icons-material';

interface ImageViewerProps {
  originalImage?: string;
  annotatedImage?: string;
  title?: string;
}

const ImageViewer: React.FC<ImageViewerProps> = ({
  originalImage,
  annotatedImage,
  title = '檢測結果'
}) => {
  if (!originalImage && !annotatedImage) {
    return (
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: 400,
          color: 'text.secondary'
        }}
      >
        <ImageIcon sx={{ fontSize: 64, mb: 2, opacity: 0.3 }} />
        <Typography variant="h6" gutterBottom>
          尚無圖像顯示
        </Typography>
        <Typography variant="body2" color="text.secondary">
          上傳圖像並運行處理以查看結果
        </Typography>
      </Box>
    );
  }

  const displayImage = annotatedImage || originalImage;

  return (
    <Box>
      <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider', bgcolor: '#fafafa' }}>
        <Typography variant="h6">{title}</Typography>
      </Box>
      <Box
        sx={{
          p: 3,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: 400,
          bgcolor: '#f9f9f9'
        }}
      >
        {displayImage && (
          <Box
            component="img"
            src={displayImage.startsWith('data:') ? displayImage : `data:image/png;base64,${displayImage}`}
            alt="檢測結果"
            sx={{
              maxWidth: '100%',
              maxHeight: 600,
              objectFit: 'contain',
              borderRadius: 1,
              boxShadow: 2
            }}
          />
        )}
      </Box>
    </Box>
  );
};

export default ImageViewer;
