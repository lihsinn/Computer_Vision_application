# 🤖 3D機械手臂智能分揀模擬器 - 設計文件

## 專案概述

建立一個3D視覺化的智能分揀系統，模擬機械手臂自動檢測並分揀物件的完整流程。

### 核心功能
1. **3D場景展示** - 使用Three.js渲染真實感的工作環境
2. **自動連續模擬** - 物件自動出現、檢測、分揀
3. **影像分割檢測** - 整合現有AOI檢測API
4. **智能分揀** - 根據檢測結果放置到正確/錯誤區
5. **即時統計報表** - 動態顯示處理結果

---

## 🎨 3D場景設計

### 場景佈局

```
                 [相機視角 - 俯視圖]

    ┌─────────────────────────────────────────┐
    │                                         │
    │   [正確區]        [錯誤區]              │
    │   ✅ PASS        ❌ NG                  │
    │   ┌─────┐        ┌─────┐                │
    │   │ 🔲 │        │ 🔲 │                │
    │   │ 🔲 │        │ 🔲 │                │
    │   └─────┘        └─────┘                │
    │                                         │
    │         [機械手臂]                       │
    │           🦾                            │
    │            ↑                            │
    │            │                            │
    │   [拍照/檢測位置]                        │
    │         📷                              │
    │            ↑                            │
    │   ═══════════════════                   │
    │     [傳送帶]  →→→                       │
    │         🔲 🔲                           │
    │                                         │
    └─────────────────────────────────────────┘
```

### 3D元件清單

| 元件 | 說明 | 材質/顏色 |
|------|------|-----------|
| **傳送帶** | 平面移動帶，物件從右側進入 | 灰色金屬質感 |
| **機械手臂** | 6自由度關節手臂 | 工業藍/銀色 |
| **夾爪** | 手臂末端執行器 | 黑色橡膠質感 |
| **相機** | 拍照裝置（視覺效果） | 黑色 |
| **正確區容器** | 綠色透明容器 | 綠色半透明 |
| **錯誤區容器** | 紅色透明容器 | 紅色半透明 |
| **待檢物件** | 螺絲、零件等 | 金屬質感 |
| **工作台** | 底座平台 | 白色/灰色 |
| **光源** | 環境光+聚光燈 | - |

---

## 🎬 動畫流程設計

### 完整分揀週期

```typescript
// 階段1: 物件進場 (2秒)
物件在傳送帶右側生成
→ 傳送帶移動
→ 物件到達檢測位置
→ 傳送帶停止

// 階段2: 拍照檢測 (1秒)
相機閃光效果
→ 截取物件影像
→ 呼叫後端API檢測
→ 等待結果

// 階段3: 手臂移動到物件 (1.5秒)
手臂關節旋轉
→ 末端移動到物件上方
→ 夾爪打開

// 階段4: 抓取物件 (0.5秒)
手臂下降
→ 夾爪閉合
→ 手臂上升

// 階段5: 移動到目標區 (2秒)
根據檢測結果選擇目標區
→ 手臂移動到正確區/錯誤區上方
→ 手臂下降

// 階段6: 放置物件 (0.5秒)
夾爪打開
→ 物件落下
→ 手臂返回初始位置

// 階段7: 統計更新 (即時)
更新處理數量
→ 更新良率
→ 重複循環
```

**總週期時間**: 約7-8秒/個物件

---

## 🏗️ 技術架構

### 前端技術棧

```typescript
React 18
├─ @react-three/fiber       // Three.js的React封裝
├─ @react-three/drei         // Three.js輔助工具
├─ three                     // 核心3D引擎
├─ @react-spring/three       // 3D動畫庫
├─ zustand                   // 狀態管理
└─ Material-UI               // UI組件
```

### 專案結構

```
frontend/src/
├─ pages/
│  └─ RoboticArmSimulator.tsx        // 主頁面
├─ components/
│  ├─ 3d/
│  │  ├─ Scene3D.tsx                 // 3D場景容器
│  │  ├─ RoboticArm.tsx              // 機械手臂組件
│  │  ├─ ConveyorBelt.tsx            // 傳送帶組件
│  │  ├─ DetectionZone.tsx           // 檢測區域
│  │  ├─ SortingBins.tsx             // 分揀容器（正確/錯誤區）
│  │  ├─ WorkPiece.tsx               // 待檢物件
│  │  ├─ Camera3D.tsx                // 虛擬相機
│  │  └─ Lighting.tsx                // 光源設置
│  ├─ simulator/
│  │  ├─ ControlPanel.tsx            // 控制面板
│  │  ├─ StatisticsPanel.tsx         // 統計報表
│  │  └─ SpeedControl.tsx            // 速度控制
│  └─ ...
├─ hooks/
│  ├─ useSimulation.ts               // 模擬邏輯Hook
│  ├─ useArmAnimation.ts             // 手臂動畫Hook
│  └─ useDetection.ts                // 檢測邏輯Hook
├─ services/
│  └─ api.ts                         // API服務（已有）
└─ store/
   └─ simulatorStore.ts              // 模擬器狀態管理
```

---

## 🔧 核心實作細節

### 1. 機械手臂建模

使用簡化的6DOF（六自由度）手臂：

```typescript
interface ArmJoint {
  id: string;
  angle: number;        // 當前角度
  minAngle: number;     // 最小角度
  maxAngle: number;     // 最大角度
  axis: 'x' | 'y' | 'z'; // 旋轉軸
}

const armStructure = {
  base: { position: [0, 0, 0], rotation: 0 },
  shoulder: { position: [0, 1, 0], rotation: 0 },
  elbow: { position: [0, 2, 0], rotation: 0 },
  wrist1: { position: [0, 3, 0], rotation: 0 },
  wrist2: { position: [0, 3.5, 0], rotation: 0 },
  gripper: { position: [0, 4, 0], open: true }
};
```

### 2. 反向運動學 (IK)

使用簡化的IK算法計算手臂關節角度：

```typescript
function calculateIK(
  targetPosition: Vector3,
  armConfig: ArmStructure
): JointAngles {
  // 簡化版IK - 使用幾何解法
  // 在實際應用中可使用更精確的FABRIK算法
  const { x, y, z } = targetPosition;
  const baseAngle = Math.atan2(x, z);
  const armLength = calculateArmReach(armConfig);
  const shoulderAngle = calculateShoulderAngle(y, armLength);

  return {
    base: baseAngle,
    shoulder: shoulderAngle,
    elbow: calculateElbowAngle(shoulderAngle),
    // ... 其他關節
  };
}
```

### 3. 物件檢測整合

```typescript
async function detectObject(objectImage: ImageData) {
  try {
    // 1. 將3D場景截圖轉為圖片
    const imageBlob = await captureObjectImage(objectImage);

    // 2. 上傳到後端
    const uploadResult = await api.uploadImage(imageBlob);

    // 3. 呼叫檢測API
    const detection = await api.detectDefects(
      uploadResult.image_id,
      threshold: 30
    );

    // 4. 判定結果
    const isPass = detection.defects.length === 0;

    return {
      result: isPass ? 'PASS' : 'NG',
      confidence: detection.confidence,
      defectCount: detection.defects.length
    };
  } catch (error) {
    console.error('Detection failed:', error);
    return { result: 'NG', confidence: 0, defectCount: -1 };
  }
}
```

### 4. 狀態管理

使用Zustand管理全局狀態：

```typescript
interface SimulatorState {
  // 模擬狀態
  isRunning: boolean;
  isPaused: boolean;
  speed: number;

  // 統計數據
  stats: {
    totalProcessed: number;
    passCount: number;
    ngCount: number;
    yieldRate: number;
  };

  // 物件隊列
  objects: WorkPiece[];
  currentObject: WorkPiece | null;

  // 手臂狀態
  armState: 'idle' | 'moving' | 'gripping' | 'releasing';

  // 動作
  start: () => void;
  pause: () => void;
  reset: () => void;
  updateStats: (result: 'PASS' | 'NG') => void;
}
```

---

## 📊 統計報表設計

### 即時顯示卡片

```typescript
<Grid container spacing={2}>
  <Grid item xs={3}>
    <StatCard
      title="總處理數"
      value={stats.totalProcessed}
      icon={<InboxIcon />}
      color="primary"
    />
  </Grid>

  <Grid item xs={3}>
    <StatCard
      title="正確數 (PASS)"
      value={stats.passCount}
      icon={<CheckCircleIcon />}
      color="success"
    />
  </Grid>

  <Grid item xs={3}>
    <StatCard
      title="錯誤數 (NG)"
      value={stats.ngCount}
      icon={<CancelIcon />}
      color="error"
    />
  </Grid>

  <Grid item xs={3}>
    <StatCard
      title="良率"
      value={`${stats.yieldRate.toFixed(2)}%`}
      icon={<TrendingUpIcon />}
      color="info"
    />
  </Grid>
</Grid>
```

### 歷史圖表

- **折線圖**: 即時良率趨勢
- **圓餅圖**: PASS/NG分佈
- **長條圖**: 每小時處理量

---

## 🎮 控制面板設計

```typescript
<ControlPanel>
  {/* 主要控制 */}
  <ButtonGroup>
    <Button onClick={start} disabled={isRunning}>
      <PlayArrowIcon /> 開始
    </Button>
    <Button onClick={pause} disabled={!isRunning}>
      <PauseIcon /> 暫停
    </Button>
    <Button onClick={reset}>
      <RefreshIcon /> 重置
    </Button>
  </ButtonGroup>

  {/* 速度控制 */}
  <Slider
    label="模擬速度"
    value={speed}
    onChange={setSpeed}
    min={0.5}
    max={3}
    step={0.1}
  />

  {/* 視角控制 */}
  <Select label="相機視角">
    <MenuItem value="top">俯視圖</MenuItem>
    <MenuItem value="side">側視圖</MenuItem>
    <MenuItem value="front">正視圖</MenuItem>
    <MenuItem value="free">自由視角</MenuItem>
  </Select>

  {/* 檢測參數 */}
  <TextField
    label="檢測閾值"
    type="number"
    value={threshold}
    onChange={setThreshold}
  />
</ControlPanel>
```

---

## 🚀 實作階段規劃

### 階段1: 基礎場景建立 (2-3小時)
- [x] 安裝Three.js相關套件
- [ ] 建立基礎3D場景
- [ ] 設置相機和光源
- [ ] 實現視角控制

### 階段2: 靜態模型建立 (3-4小時)
- [ ] 建立傳送帶模型
- [ ] 建立簡化版機械手臂
- [ ] 建立分揀容器
- [ ] 建立待檢物件

### 階段3: 動畫系統 (4-5小時)
- [ ] 實現傳送帶動畫
- [ ] 實現手臂關節動畫
- [ ] 實現物件移動動畫
- [ ] 實現抓取/放置動作

### 階段4: 檢測整合 (2-3小時)
- [ ] 場景截圖功能
- [ ] API呼叫整合
- [ ] 結果處理邏輯

### 階段5: UI與統計 (2-3小時)
- [ ] 控制面板
- [ ] 統計報表
- [ ] 圖表顯示

### 階段6: 優化與測試 (2小時)
- [ ] 效能優化
- [ ] 動畫流暢度調整
- [ ] 錯誤處理

**總開發時間預估**: 15-20小時

---

## 📦 需要安裝的套件

```bash
npm install three @react-three/fiber @react-three/drei
npm install @react-spring/three
npm install zustand
npm install recharts  # 統計圖表
```

---

## 💡 進階功能（可選）

1. **多手臂協同** - 兩個手臂同時工作
2. **瑕疵類型分類** - 細分NG原因
3. **學習模式** - 記錄誤判並改進
4. **VR/AR支援** - 使用VR裝置查看
5. **真實設備連接** - 與實際機械手臂通訊
6. **物理引擎** - 更真實的物理效果
7. **錄影功能** - 匯出模擬過程影片

---

## 🔍 參考資源

- **Three.js官方文檔**: https://threejs.org/docs/
- **React Three Fiber**: https://docs.pmnd.rs/react-three-fiber/
- **機械手臂IK算法**: FABRIK (Forward And Backward Reaching Inverse Kinematics)
- **3D模型資源**: Sketchfab, TurboSquid

---

## 下一步行動

您想要我現在開始實作嗎？我建議：

1. **先做原型** - 快速建立基礎場景，看效果是否符合預期
2. **逐步完善** - 先做簡單的2D平面手臂，確認邏輯正確後再升級3D
3. **模組化開發** - 一次完成一個組件，便於測試

請告訴我：
- ✅ 開始實作基礎場景
- 🔄 先做簡化原型看效果
- 💬 討論更多細節
