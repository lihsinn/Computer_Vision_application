# Computer Vision Application

整合數學學習與 AOI 系統開發的完整專案

## 📁 專案結構

```
computer-vision-application/
├── practice/              # 數學與程式學習教材
│   ├── 1_linear_algebra/
│   ├── 2_calculus_kinematics/
│   ├── 3_image_processing/
│   ├── 4_control_theory/
│   └── README.md
│
└── aoi-system/           # AOI 檢測系統（實戰專案）
    ├── backend/          # Flask API
    └── frontend/         # React UI
```

## 🎯 學習路徑

### 階段一：基礎學習 (practice/)
從零開始學習 AOI/上位機開發所需的數學和程式技能

1. **線性代數** - 向量、矩陣、旋轉、座標變換
2. **微積分與運動學** - 速度、加速度、PID、MPC
3. **影像處理** - OpenCV 基礎與 AOI 應用
4. **控制理論** - 系統建模、穩定性、頻率響應

### 階段二：實戰應用 (aoi-system/)
將所學知識整合成完整的 AOI 檢測系統

- 模擬相機系統
- 瑕疵自動檢測
- 運動平台控制
- Web 介面操作
- 報表生成

## 🚀 快速開始

### 學習教材

```bash
cd practice
pip install -r requirements.txt
python 1_linear_algebra/01_vectors_matrices.py
```

### AOI 系統

**Backend:**
```bash
cd aoi-system/backend
pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
cd aoi-system/frontend
npm install
npm start
```

## 💡 特色

✅ **完全模擬** - 無需硬體即可學習和開發
✅ **實用導向** - 所有程式碼都可用於實際專案
✅ **循序漸進** - 從基礎數學到完整系統
✅ **豐富範例** - 包含大量視覺化和練習題

## 📚 技術棧

**Learning (practice/):**
- Python 3.8+
- NumPy, SciPy
- OpenCV
- Matplotlib

**Application (aoi-system/):**
- Backend: Flask, Flask-SocketIO
- Frontend: React, Socket.IO
- Image Processing: OpenCV
- Control: Custom PID/MPC

## 🎓 學習建議

1. **初學者**：先完成 practice 資料夾的所有教材
2. **有基礎者**：可以直接參考感興趣的主題
3. **實戰開發**：完成基礎學習後，進入 aoi-system 實作

## 📖 詳細文檔

- [學習教材說明](practice/README.md)
- [AOI 系統文檔](aoi-system/README.md)

## 🤝 貢獻

歡迎提出問題和建議！

## 📄 授權

MIT License - 自由使用和修改
