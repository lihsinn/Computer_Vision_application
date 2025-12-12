import React, { useState, useRef } from 'react';
import { Box, Typography, Paper, CircularProgress } from '@mui/material';
import { CloudUpload } from '@mui/icons-material';
import { api } from '../services/api';
import { UploadResponse } from '../types/aoi.types';

interface ImageUploadProps {
  onUploadSuccess: (response: UploadResponse) => void;
  onError: (error: string) => void;
}

const ImageUpload: React.FC<ImageUploadProps> = ({ onUploadSuccess, onError }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleDragEnter = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      handleFile(files[0]);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      handleFile(files[0]);
    }
  };

  const handleFile = async (file: File) => {
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/bmp', 'image/tiff'];
    if (!validTypes.includes(file.type)) {
      onError('無效的文件類型。請上傳 PNG, JPG, BMP 或 TIFF 圖像。');
      return;
    }

    if (file.size > 16 * 1024 * 1024) {
      onError('文件太大。最大大小為 16MB。');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      setPreviewUrl(e.target?.result as string);
    };
    reader.readAsDataURL(file);

    setIsUploading(true);
    try {
      const response = await api.uploadImage(file);
      onUploadSuccess(response);
    } catch (error: any) {
      const errorMessage = error.response?.data?.error?.message || '上傳失敗';
      onError(errorMessage);
      setPreviewUrl(null);
    } finally {
      setIsUploading(false);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <Box>
      <Paper
        elevation={isDragging ? 8 : 2}
        sx={{
          p: 3,
          textAlign: 'center',
          cursor: 'pointer',
          border: isDragging ? '2px dashed #667eea' : '2px dashed #ddd',
          bgcolor: isDragging ? '#f0f4ff' : '#fafafa',
          transition: 'all 0.3s ease',
          '&:hover': {
            borderColor: '#667eea',
            bgcolor: '#f9fafb'
          }
        }}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />

        {previewUrl ? (
          <Box>
            <Box
              component="img"
              src={previewUrl}
              alt="Preview"
              sx={{
                maxWidth: '100%',
                maxHeight: 200,
                objectFit: 'contain',
                borderRadius: 1,
                mb: 1
              }}
            />
            <Typography variant="caption" color="text.secondary">
              點擊或拖拽以更換圖像
            </Typography>
          </Box>
        ) : (
          <Box>
            {isUploading ? (
              <>
                <CircularProgress size={48} sx={{ mb: 2 }} />
                <Typography>上傳中...</Typography>
              </>
            ) : (
              <>
                <CloudUpload sx={{ fontSize: 64, color: '#667eea', mb: 2 }} />
                <Typography variant="h6" gutterBottom>
                  上傳圖像
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  拖拽圖像到此處，或點擊選擇文件
                </Typography>
                <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                  支持: PNG, JPG, BMP, TIFF (最大 16MB)
                </Typography>
              </>
            )}
          </Box>
        )}
      </Paper>
    </Box>
  );
};

export default ImageUpload;
