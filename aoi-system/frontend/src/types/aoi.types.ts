/**
 * TypeScript Type Definitions for AOI System
 */

export interface Position {
  x: number;
  y: number;
}

export interface BoundingBox {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface Size {
  width: number;
  height: number;
}

export interface Defect {
  id: number;
  position: Position;
  area: number;
  bbox: BoundingBox;
}

export interface Measurement {
  object_id: number;
  shape: 'rectangle' | 'circle';
  width_mm: number;
  height_mm: number;
  area_mm2: number;
  bbox: BoundingBox;
  diameter_mm?: number;  // For circles
}

export interface FiducialMark {
  id: number;
  position: Position;
  radius: number;
}

export interface DefectDetectionResult {
  success: boolean;
  defects: Defect[];
  defect_count: number;
  annotated_image: string;  // base64
}

export interface MeasurementResult {
  success: boolean;
  measurements: Measurement[];
  annotated_image: string;  // base64
}

export interface FiducialDetectionResult {
  success: boolean;
  marks: FiducialMark[];
  rotation_angle: number | null;
  annotated_image: string;  // base64
}

export interface UploadResponse {
  success: boolean;
  image_id: string;
  filename: string;
  size: Size;
}

export interface ApiError {
  code: string;
  message: string;
  details: string;
}

export interface ErrorResponse {
  success: false;
  error: ApiError;
}

export type ProcessingMode = 'defect' | 'measurement' | 'fiducial';

export interface ProcessingConfig {
  mode: ProcessingMode;
  threshold?: number;  // For defect detection
  calibration?: number;  // pixel_to_mm for measurement
  minRadius?: number;  // For fiducial detection
  maxRadius?: number;  // For fiducial detection
}
