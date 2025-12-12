/**
 * API Service Layer
 * Handles all HTTP requests to Flask backend
 */
import axios, { AxiosInstance } from 'axios';
import {
  UploadResponse,
  DefectDetectionResult,
  MeasurementResult,
  FiducialDetectionResult,
  ErrorResponse
} from '../types/aoi.types';

const API_BASE = 'http://localhost:5000/api';

class APIService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE,
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  /**
   * Upload an image file
   */
  async uploadImage(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('image', file);

    const response = await this.client.post<UploadResponse>('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  }

  /**
   * Detect defects in uploaded image
   */
  async detectDefects(
    imageId: string,
    threshold: number = 30,
    templateId?: string
  ): Promise<DefectDetectionResult> {
    const response = await this.client.post<DefectDetectionResult>('/process/defect-detection', {
      image_id: imageId,
      template_id: templateId,
      threshold,
    });

    return response.data;
  }

  /**
   * Measure dimensions in image
   */
  async measureDimensions(
    imageId: string,
    pixelToMm: number = 0.1
  ): Promise<MeasurementResult> {
    const response = await this.client.post<MeasurementResult>('/process/measurement', {
      image_id: imageId,
      calibration: { pixel_to_mm: pixelToMm },
    });

    return response.data;
  }

  /**
   * Detect fiducial marks
   */
  async detectFiducialMarks(
    imageId: string,
    minRadius: number = 5,
    maxRadius: number = 25
  ): Promise<FiducialDetectionResult> {
    const response = await this.client.post<FiducialDetectionResult>('/process/fiducial-detection', {
      image_id: imageId,
      min_radius: minRadius,
      max_radius: maxRadius,
    });

    return response.data;
  }

  /**
   * Check API health
   */
  async healthCheck(): Promise<{ status: string; message: string; database?: string }> {
    const response = await this.client.get('/health');
    return response.data;
  }

  /**
   * Create a new lot (批次)
   */
  async createLot(lotNumber: string, description?: string): Promise<any> {
    const response = await this.client.post('/lots', {
      lot_number: lotNumber,
      description,
    });
    return response.data;
  }

  /**
   * Get all lots
   */
  async getLots(status?: string): Promise<any> {
    const params = status ? { status } : {};
    const response = await this.client.get('/lots', { params });
    return response.data;
  }

  /**
   * Get lot by ID
   */
  async getLot(lotId: string): Promise<any> {
    const response = await this.client.get(`/lots/${lotId}`);
    return response.data;
  }

  /**
   * Create inspection record (檢測記錄)
   */
  async createInspection(data: {
    lot_id: string;
    serial_number: string;
    side: 'A' | 'B';
    inspection_mode: 'Run' | 'OfflineTest';
    inspection_type: 'SingleInsp' | 'BatchInsp';
    image_path: string;
    annotated_image_path?: string;
    cells: any[];
    defects: any;
    threshold?: number;
    running_result?: string;
    positioning_abnormal?: boolean;
  }): Promise<any> {
    const response = await this.client.post('/inspections', data);
    return response.data;
  }

  /**
   * Get inspection by ID
   */
  async getInspection(inspectionId: string): Promise<any> {
    const response = await this.client.get(`/inspections/${inspectionId}`);
    return response.data;
  }

  /**
   * Get all inspections
   */
  async getInspections(filters?: {
    lot_id?: string;
    serial_number?: string;
    side?: string;
  }): Promise<any> {
    const response = await this.client.get('/inspections', { params: filters });
    return response.data;
  }

  /**
   * Get cells for inspection
   */
  async getInspectionCells(inspectionId: string): Promise<any> {
    const response = await this.client.get(`/inspections/${inspectionId}/cells`);
    return response.data;
  }
}

// Export singleton instance
export const api = new APIService();
export default api;
