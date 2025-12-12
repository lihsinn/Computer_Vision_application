# AOI 檢測系統 (MUI版本)
**使用 React + TypeScript + Material-UI + Flask + OpenCV**

---

## 🎨 更新內容

### 前端技術棧
- ✅ **React 18** - 現代化UI框架
- ✅ **TypeScript** - 類型安全
- ✅ **Material-UI (MUI) v5** - Google Material Design UI組件庫
- ✅ **Emotion** - CSS-in-JS樣式方案
- ✅ **Axios** - HTTP客戶端

### 後端技術棧
- ✅ **Flask 3.0** - Python Web框架
- ✅ **OpenCV 4.8** - 計算機視覺
- ✅ **NumPy** - 數值計算

---

## 📦 安裝依賴

### 後端依賴
```bash
cd aoi-system/backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 前端依賴（已自動安裝）
```bash
cd aoi-system/frontend
npm install  # 已包含MUI相關套件
```

**已安裝的MUI套件：**
- @mui/material
- @mui/icons-material
- @emotion/react
- @emotion/styled

---

## 🚀 啟動系統

### 方法1：使用啟動腳本（Windows）
```
1. 雙擊 start-backend.bat
2. 雙擊 start-frontend.bat
3. 瀏覽器自動打開 http://localhost:5173
```

### 方法2：手動啟動

**後端（終端1）：**
```bash
cd aoi-system/backend
venv\Scripts\activate
python run.py
```
後端運行在: http://localhost:5000

**前端（終端2）：**
```bash
cd aoi-system/frontend
npm run dev
```
前端運行在: http://localhost:5173

---

## 🎯 使用指南

### 1. 上傳圖像
- 點擊上傳區域或拖拽圖像文件
- 支持: PNG, JPG, BMP, TIFF (最大16MB)
- 即時預覽

### 2. 選擇處理模式

#### 🔍 瑕疵檢測
- 自動識別圖像中的缺陷和異常
- 調整閾值參數 (10-100)
- 顯示瑕疵位置、面積和邊界框

#### 📏 尺寸測量
- 測量物體的寬度、高度、面積
- 設置校準係數（像素到毫米）
- 自動識別矩形和圓形

#### 🎯 定位標記檢測
- 檢測圓形定位標記
- 計算旋轉角度
- 可調整半徑範圍

### 3. 查看結果
- 左側：處理控制面板
- 右側上：檢測結果圖像
- 右側下：詳細數據表格（使用MUI表格組件）

---

## 🎨 MUI 組件使用

### 主要使用的MUI組件

#### 佈局組件
- `Container` - 響應式容器
- `Grid` - 柵格系統
- `Box` - 靈活的盒子容器
- `Paper` - 卡片容器

#### 輸入組件
- `Button` / `ButtonGroup` - 按鈕
- `TextField` - 文本輸入
- `Slider` - 滑桿

#### 數據顯示
- `Table` / `TableContainer` - 表格
- `Tabs` / `Tab` - 標籤頁
- `Chip` - 標籤
- `Typography` - 文字排版

#### 反饋組件
- `Alert` - 警告提示
- `CircularProgress` - 加載動畫

#### 圖標
- `BugReport` - 瑕疵檢測圖標
- `Straighten` - 測量圖標
- `GpsFixed` - 定位標記圖標
- `CloudUpload` - 上傳圖標

---

## 🎨 界面預覽

### 主要特點
1. **Material Design** 風格UI
2. **響應式佈局** - 自適應不同屏幕
3. **優雅的動畫** - 平滑過渡效果
4. **專業的配色** - 漸變色AppBar
5. **清晰的層次** - Paper陰影效果

### 顏色主題
- 主色調：紫色漸變 (#667eea → #764ba2)
- 成功色：綠色 (success)
- 錯誤色：紅色 (error)
- 警告色：橙色 (warning)
- 信息色：藍色 (primary)

---

## 📁 項目結構

```
aoi-system/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ImageUpload.tsx      ← MUI Paper, CloudUpload
│   │   │   ├── ImageViewer.tsx      ← MUI Box, Typography
│   │   │   └── ResultsPanel.tsx     ← MUI Table, Tabs, Chip
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── types/
│   │   │   └── aoi.types.ts
│   │   ├── App.tsx                   ← MUI AppBar, Grid, Container
│   │   └── main.tsx                  ← CssBaseline
│   └── package.json                  ← 包含所有MUI依賴
│
└── backend/
    ├── app/
    │   ├── routes/
    │   │   ├── upload.py
    │   │   └── process.py
    │   ├── services/
    │   │   ├── image_handler.py
    │   │   └── aoi_service.py
    │   └── __init__.py
    ├── requirements.txt
    └── run.py
```

---

## 🔧 開發說明

### 自定義MUI主題
在 `frontend/src/main.tsx` 中添加主題：

```tsx
import { createTheme, ThemeProvider } from '@mui/material';

const theme = createTheme({
  palette: {
    primary: {
      main: '#667eea',
    },
    secondary: {
      main: '#764ba2',
    },
  },
});

// 在 App 外層包裹 ThemeProvider
<ThemeProvider theme={theme}>
  <App />
</ThemeProvider>
```

### 添加新組件
使用 MUI 組件庫：
```tsx
import { Button, TextField, Dialog } from '@mui/material';
import { Add, Delete, Edit } from '@mui/icons-material';
```

### 響應式設計
使用 MUI 的 Grid 系統：
```tsx
<Grid container spacing={2}>
  <Grid item xs={12} md={6} lg={4}>
    {/* 移動端全寬，平板半寬，桌面1/3寬 */}
  </Grid>
</Grid>
```

---

## 常見問題

### Q: MUI樣式不生效
**A:** 確認已安裝 @emotion/react 和 @emotion/styled

### Q: 圖標顯示不出來
**A:** 確認已安裝 @mui/icons-material
```bash
npm install @mui/icons-material
```

### Q: 想要修改主題顏色
**A:** 創建自定義主題並使用 ThemeProvider

### Q: 組件報類型錯誤
**A:** 確認 TypeScript 配置正確，檢查 @types 包

---

## 📚 參考資源

- [MUI 官方文檔](https://mui.com/)
- [MUI 組件庫](https://mui.com/material-ui/getting-started/)
- [MUI 圖標列表](https://mui.com/material-ui/material-icons/)
- [Emotion 文檔](https://emotion.sh/docs/introduction)

---

## 🎉 完成！

現在你有一個完整的、使用 Material-UI 設計的 AOI 檢測系統！

**特點：**
- ✅ 現代化 UI 設計
- ✅ 完整的 TypeScript 類型支持
- ✅ 響應式佈局
- ✅ Material Design 規範
- ✅ 優雅的動畫效果
- ✅ 專業的數據展示

**立即開始使用！** 🚀
