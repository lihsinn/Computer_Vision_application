/**
 * Robotic Arm Simulator State Management
 * 使用Zustand管理模擬器全局狀態
 */

import { create } from 'zustand';

// 物件介面
export interface WorkPiece {
  id: string;
  position: [number, number, number];
  rotation: [number, number, number];
  status: 'queue' | 'detecting' | 'gripped' | 'sorted' | 'completed';
  detectionResult?: 'PASS' | 'NG';
  detectionConfidence?: number;
  defectCount?: number;
}

// 機械手臂狀態
export type ArmState = 'idle' | 'moving_to_object' | 'gripping' | 'moving_to_bin' | 'releasing';

// 統計數據
export interface Statistics {
  totalProcessed: number;
  passCount: number;
  ngCount: number;
  yieldRate: number;
  currentSpeed: number;
  startTime?: Date;
  elapsedTime: number;
}

// 模擬器狀態介面
interface SimulatorState {
  // 運行狀態
  isRunning: boolean;
  isPaused: boolean;
  speed: number; // 1.0 = 正常速度, 2.0 = 2倍速

  // 物件管理
  workPieces: WorkPiece[];
  currentWorkPiece: WorkPiece | null;
  nextWorkPieceId: number;

  // 手臂狀態
  armState: ArmState;
  armTarget: [number, number, number] | null;
  gripperOpen: boolean;

  // 統計數據
  stats: Statistics;

  // 視角控制
  cameraView: 'top' | 'side' | 'front' | 'free';

  // 檢測參數
  threshold: number;

  // 動作
  start: () => void;
  pause: () => void;
  resume: () => void;
  reset: () => void;
  setSpeed: (speed: number) => void;
  setCameraView: (view: 'top' | 'side' | 'front' | 'free') => void;
  setThreshold: (threshold: number) => void;

  // 物件管理
  addWorkPiece: () => void;
  updateWorkPiece: (id: string, updates: Partial<WorkPiece>) => void;
  removeWorkPiece: (id: string) => void;
  setCurrentWorkPiece: (piece: WorkPiece | null) => void;

  // 手臂控制
  setArmState: (state: ArmState) => void;
  setArmTarget: (target: [number, number, number] | null) => void;
  setGripperOpen: (open: boolean) => void;

  // 統計更新
  updateStats: (result: 'PASS' | 'NG') => void;
  updateElapsedTime: () => void;
}

// 建立Store
export const useSimulatorStore = create<SimulatorState>((set, get) => ({
  // 初始狀態
  isRunning: false,
  isPaused: false,
  speed: 1.0,

  workPieces: [],
  currentWorkPiece: null,
  nextWorkPieceId: 1,

  armState: 'idle',
  armTarget: null,
  gripperOpen: true,

  stats: {
    totalProcessed: 0,
    passCount: 0,
    ngCount: 0,
    yieldRate: 0,
    currentSpeed: 0,
    elapsedTime: 0,
  },

  cameraView: 'free',
  threshold: 30,

  // 動作實作
  start: () => {
    const state = get();
    if (!state.isRunning) {
      set({
        isRunning: true,
        isPaused: false,
        stats: {
          ...state.stats,
          startTime: new Date(),
        },
      });
    }
  },

  pause: () => {
    set({ isPaused: true });
  },

  resume: () => {
    set({ isPaused: false });
  },

  reset: () => {
    set({
      isRunning: false,
      isPaused: false,
      speed: 1.0,
      workPieces: [],
      currentWorkPiece: null,
      nextWorkPieceId: 1,
      armState: 'idle',
      armTarget: null,
      gripperOpen: true,
      stats: {
        totalProcessed: 0,
        passCount: 0,
        ngCount: 0,
        yieldRate: 0,
        currentSpeed: 0,
        elapsedTime: 0,
      },
      cameraView: 'free',
      threshold: 30,
    });
  },

  setSpeed: (speed: number) => {
    set({ speed: Math.max(0.1, Math.min(5.0, speed)) });
  },

  setCameraView: (view) => {
    set({ cameraView: view });
  },

  setThreshold: (threshold: number) => {
    set({ threshold: Math.max(10, Math.min(100, threshold)) });
  },

  // 物件管理實作
  addWorkPiece: () => {
    const state = get();
    const newPiece: WorkPiece = {
      id: `piece-${state.nextWorkPieceId}`,
      position: [5, 0.5, 0], // 傳送帶右側起點
      rotation: [0, 0, 0],
      status: 'queue',
    };

    set({
      workPieces: [...state.workPieces, newPiece],
      nextWorkPieceId: state.nextWorkPieceId + 1,
    });
  },

  updateWorkPiece: (id, updates) => {
    set((state) => ({
      workPieces: state.workPieces.map((piece) =>
        piece.id === id ? { ...piece, ...updates } : piece
      ),
    }));
  },

  removeWorkPiece: (id) => {
    set((state) => ({
      workPieces: state.workPieces.filter((piece) => piece.id !== id),
    }));
  },

  setCurrentWorkPiece: (piece) => {
    set({ currentWorkPiece: piece });
  },

  // 手臂控制實作
  setArmState: (state) => {
    set({ armState: state });
  },

  setArmTarget: (target) => {
    set({ armTarget: target });
  },

  setGripperOpen: (open) => {
    set({ gripperOpen: open });
  },

  // 統計更新實作
  updateStats: (result) => {
    set((state) => {
      const newTotalProcessed = state.stats.totalProcessed + 1;
      const newPassCount =
        result === 'PASS' ? state.stats.passCount + 1 : state.stats.passCount;
      const newNgCount = result === 'NG' ? state.stats.ngCount + 1 : state.stats.ngCount;
      const newYieldRate =
        newTotalProcessed > 0 ? (newPassCount / newTotalProcessed) * 100 : 0;

      return {
        stats: {
          ...state.stats,
          totalProcessed: newTotalProcessed,
          passCount: newPassCount,
          ngCount: newNgCount,
          yieldRate: newYieldRate,
        },
      };
    });
  },

  updateElapsedTime: () => {
    set((state) => {
      if (!state.stats.startTime) return state;

      const elapsed = Date.now() - state.stats.startTime.getTime();
      const elapsedSeconds = Math.floor(elapsed / 1000);

      // 計算當前處理速度 (件/小時)
      const itemsPerSecond = elapsedSeconds > 0 ? state.stats.totalProcessed / elapsedSeconds : 0;
      const itemsPerHour = itemsPerSecond * 3600;

      return {
        stats: {
          ...state.stats,
          elapsedTime: elapsedSeconds,
          currentSpeed: itemsPerHour,
        },
      };
    });
  },
}));
