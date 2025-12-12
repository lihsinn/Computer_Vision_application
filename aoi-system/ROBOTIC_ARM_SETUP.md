# 🤖 3D機械手臂模擬器 - 安裝與啟動指南

## ✅ 已完成功能

### 核心功能
- ✅ **3D場景渲染** - 使用Three.js建立真實感的工作環境
- ✅ **機械手臂模型** - 6自由度關節手臂，帶夾爪
- ✅ **傳送帶系統** - 動畫傳送帶，物件自動移動
- ✅ **智能分揀** - 自動檢測並分類到正確/錯誤區
- ✅ **即時統計** - 良率、處理數量、速度等統計資訊
- ✅ **控制面板** - 開始/暫停/重置、速度調整、視角切換

### 分揀流程
```
1. 物件在傳送帶上出現
   ↓
2. 移動到檢測位置（黃色標記）
   ↓
3. 拍照檢測（模擬AI檢測）
   ↓
4. 機械手臂移動並抓取物件
   ↓
5. 根據結果移動到對應區域
   ├─ ✅ PASS → 綠色容器
   └─ ❌ NG → 紅色容器
   ↓
6. 放置物件並更新統計
```

---

## 🚀 快速啟動（5分鐘）

### 步驟 1: 安裝依賴

```bash
# 進入前端目錄
cd aoi-system/frontend

# 安裝所有依賴（包含新增的Three.js套件）
npm install
```

### 步驟 2: 啟動開發伺服器

```bash
# 啟動前端
npm run dev
```

前端將在 `http://localhost:5173` 啟動

### 步驟 3: 訪問模擬器

在瀏覽器中打開：`http://localhost:5173`

目前需要將 `App.tsx` 導入模擬器頁面（見下方整合步驟）

---

## 🔧 完整整合步驟

### 方法 1: 快速測試（直接替換App.tsx）

**暫時方案**：直接在 `App.tsx` 中導入模擬器

```tsx
// frontend/src/App.tsx
import RoboticArmSimulator from './pages/RoboticArmSimulator';

function App() {
  return <RoboticArmSimulator />;
}

export default App;
```

### 方法 2: 完整路由整合（推薦）

**1. 安裝React Router**
```bash
npm install react-router-dom
```

**2. 更新 `App.tsx`**
```tsx
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Button, Box } from '@mui/material';
import RoboticArmSimulator from './pages/RoboticArmSimulator';
import SingleInspectionPage from './pages/SingleInspectionPage';

function App() {
  return (
    <BrowserRouter>
      <AppBar position="static">
        <Toolbar>
          <Button color="inherit" component={Link} to="/">
            首頁
          </Button>
          <Button color="inherit" component={Link} to="/single-inspection">
            單片檢測
          </Button>
          <Button color="inherit" component={Link} to="/robot-simulator">
            手臂模擬器
          </Button>
        </Toolbar>
      </AppBar>

      <Box sx={{ mt: 2 }}>
        <Routes>
          <Route path="/" element={<h1>AOI系統首頁</h1>} />
          <Route path="/single-inspection" element={<SingleInspectionPage />} />
          <Route path="/robot-simulator" element={<RoboticArmSimulator />} />
        </Routes>
      </Box>
    </BrowserRouter>
  );
}

export default App;
```

---

## 📦 新增的檔案結構

```
frontend/src/
├── store/
│   └── simulatorStore.ts          # Zustand狀態管理
├── components/
│   └── 3d/
│       ├── Scene3D.tsx            # 3D場景容器
│       ├── RoboticArm.tsx         # 機械手臂
│       ├── ConveyorBelt.tsx       # 傳送帶
│       ├── SortingBins.tsx        # 分揀容器
│       ├── WorkPieces.tsx         # 待檢物件
│       └── Lighting.tsx           # 光源設置
└── pages/
    └── RoboticArmSimulator.tsx    # 主頁面
```

---

## 🎮 使用說明

### 基本操作

1. **啟動模擬**
   - 點擊「開始」按鈕
   - 物件將自動生成並進入分揀流程

2. **控制速度**
   - 使用速度滑桿調整（0.5x - 3x）
   - 暫停後可調整，繼續時生效

3. **切換視角**
   - 自由視角：可旋轉、縮放
   - 俯視圖/側視圖/正視圖：固定視角

4. **查看統計**
   - 即時更新處理數量、良率
   - 顯示PASS/NG分佈
   - 計算處理速度（件/小時）

### 場景元素說明

| 元素 | 顏色 | 說明 |
|------|------|------|
| 傳送帶 | 灰色 | 物件移動軌道 |
| 檢測位置 | 黃色標記 | 拍照檢測區域 |
| 機械手臂 | 藍色 | 6自由度關節手臂 |
| 正確區 | 綠色 | PASS物件放置區 |
| 錯誤區 | 紅色 | NG物件放置區 |
| 物件 | 灰→黃→綠/紅 | 螺絲/零件，顏色表示狀態 |

### 手臂狀態指示燈

- 🟢 **綠燈** - idle（待機中）
- 🟡 **黃燈** - gripping（抓取中）
- 🔴 **紅燈** - moving（移動中）

---

## 🔗 整合現有AOI檢測API

目前模擬器使用隨機結果，要整合真實檢測：

### 修改檢測邏輯

在 `RoboticArmSimulator.tsx` 中找到這段：

```typescript
// 現在：模擬檢測（隨機結果）
const detectionResult = Math.random() > 0.3 ? 'PASS' : 'NG';
```

**替換為**：

```typescript
// 整合真實檢測API
try {
  // 1. 截取物件影像（需實作截圖功能）
  const imageData = captureObjectImage();

  // 2. 上傳到後端
  const uploadResult = await api.uploadImage(imageData);

  // 3. 呼叫檢測API
  const detection = await api.detectDefects(
    uploadResult.image_id,
    threshold
  );

  // 4. 判定結果
  const detectionResult = detection.defects.length === 0 ? 'PASS' : 'NG';

  updateWorkPiece(pieceToDetect.id, {
    detectionResult,
    defectCount: detection.defects.length,
  });
} catch (error) {
  console.error('Detection failed:', error);
  const detectionResult = 'NG'; // 檢測失敗視為NG
}
```

---

## 🐛 常見問題排查

### 問題 1: 3D場景顯示空白

**原因**: Three.js相關套件未正確安裝

**解決**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### 問題 2: 動畫卡頓

**原因**: 電腦效能不足或瀏覽器硬體加速未啟用

**解決**:
- 降低模擬速度
- 啟用瀏覽器硬體加速
- 關閉其他佔用資源的應用

### 問題 3: 手臂動作不流暢

**原因**: 動畫配置或幀率問題

**解決**:
- 調整 `react-spring` 的 config
- 檢查瀏覽器控制台錯誤
- 確認Three.js版本兼容性

### 問題 4: 缺少字體檔案

**錯誤**: `Cannot find font: /fonts/Inter-Bold.woff`

**解決**:
暫時可移除Text組件中的font屬性，或下載字體檔案：

```tsx
// 修改 SortingBins.tsx
<Text
  position={[0, 1.2, 0]}
  fontSize={0.4}
  color={labelColor}
  anchorX="center"
  anchorY="middle"
  // font="/fonts/Inter-Bold.woff"  // 暫時註解
>
  {label}
</Text>
```

---

## 📊 效能優化建議

### 1. 減少物件數量
```typescript
// 在 simulatorStore.ts 中調整
const MAX_PIECES = 3; // 限制同時存在的物件數量
```

### 2. 簡化幾何體
```typescript
// 減少幾何體的細節
<cylinderGeometry args={[0.15, 0.15, 0.4, 8]} />  // 從16改為8
```

### 3. 使用InstancedMesh
對於大量重複物件，使用InstancedMesh提升效能

---

## 🎯 下一步開發建議

### 短期改進
1. **真實物件模型** - 導入.glb/.fbx 3D模型
2. **更精確的IK** - 實作FABRIK算法
3. **碰撞檢測** - 使用物理引擎（Cannon.js）
4. **截圖功能** - 實作場景截圖用於檢測

### 中期擴展
1. **多手臂協同** - 兩個手臂同時工作
2. **瑕疵類型細分** - 顯示具體瑕疵類型
3. **歷史記錄** - 儲存每次分揀的詳細資料
4. **匯出報表** - PDF報表生成

### 長期願景
1. **VR/AR支援** - 使用WebXR查看3D場景
2. **真實設備連接** - 與實際機械手臂通訊
3. **AI訓練模式** - 記錄資料用於改進模型
4. **多場景切換** - 不同產線的模擬

---

## 📚 技術文件連結

- **Three.js文件**: https://threejs.org/docs/
- **React Three Fiber**: https://docs.pmnd.rs/react-three-fiber/
- **Zustand文件**: https://github.com/pmndrs/zustand
- **設計文件**: `ROBOTIC_ARM_SIMULATOR_DESIGN.md`

---

## 🎉 完成！

模擬器已經可以運行！執行以下命令開始體驗：

```bash
cd aoi-system/frontend
npm install
npm run dev
```

然後訪問 `http://localhost:5173`，享受3D機械手臂分揀的視覺盛宴！ 🚀
