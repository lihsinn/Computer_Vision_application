# 🚀 AOI系統快速啟動指南

## 📋 主題1已完成！

單片檢測自動儲存瑕疵工單功能已實現，包括：
- ✅ 離線檢測/執行模式切換
- ✅ 批次管理
- ✅ 自動儲存檢測記錄
- ✅ 檢測結果顯示（序號、良率%、NG顆數、定位異常等）

---

## ⚡ 5分鐘快速啟動

### 前提條件
- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

### 步驟 1: 資料庫設定（2分鐘）

```bash
# 1. 建立PostgreSQL資料庫
createdb aoi_system

# 或使用psql
psql -U postgres
CREATE DATABASE aoi_system;
\q
```

### 步驟 2: 後端設定（2分鐘）

```bash
# 進入後端目錄
cd aoi-system\backend

# 建立虛擬環境（Windows）
python -m venv venv
venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt

# 複製環境變數檔案
copy .env.example .env

# 編輯.env設定資料庫連接（使用記事本或VS Code）
# DATABASE_URL=postgresql://postgres:你的密碼@localhost:5432/aoi_system

# 初始化資料庫
python init_db.py --create

# 啟動後端
python run.py
```

後端將在 `http://localhost:5000` 運行

### 步驟 3: 前端設定（1分鐘）

**開啟新的終端機視窗**

```bash
# 進入前端目錄
cd aoi-system\frontend

# 安裝依賴（首次執行）
npm install

# 安裝React Router
npm install react-router-dom @types/react-router-dom

# 啟動前端
npm run dev
```

前端將在 `http://localhost:5173` 運行

### 步驟 4: 整合路由（可選）

如要訪問單片檢測頁面，需要在 `frontend/src/App.tsx` 中加入路由。

暫時方案：直接將 `App.tsx` 的內容替換為 `SingleInspectionPage` 進行測試。

---

## 🎯 快速測試流程

1. **開啟瀏覽器**: `http://localhost:5173`

2. **建立批次**:
   - 在「新批號」輸入框輸入 `LOT001`
   - 點擊「建立」按鈕

3. **執行檢測**:
   - 選擇剛建立的批次
   - 序號保持 `001`（自動遞增）
   - 選擇 A面
   - 點擊「選擇影像」上傳測試圖片
   - 點擊「執行檢測」

4. **查看結果**:
   - 檢測完成後，結果會顯示在右側表格
   - 底部統計卡片會更新
   - 序號自動遞增到 `002`

---

## 🛠️ 常見問題快速解決

### 問題 1: 無法連接資料庫

```bash
# 檢查PostgreSQL是否運行
# Windows: 開啟服務管理員，查找postgresql服務
# 或在cmd執行:
psql -U postgres -c "SELECT version();"
```

### 問題 2: 後端啟動失敗

```bash
# 確認虛擬環境已啟動
venv\Scripts\activate

# 重新安裝依賴
pip install -r requirements.txt --force-reinstall
```

### 問題 3: 前端無法連接後端

檢查後端是否在運行：
```
http://localhost:5000/api/health
```

應該返回：
```json
{
  "status": "healthy",
  "message": "AOI Backend is running",
  "database": "connected"
}
```

### 問題 4: 資料表不存在

```bash
# 重新初始化資料庫
python init_db.py --reset
```

**注意**: 這會刪除所有現有資料！

---

## 📂 重要檔案位置

| 檔案 | 用途 |
|------|------|
| `backend/SETUP_GUIDE.md` | 詳細後端設定指南 |
| `backend/database_design.md` | 資料庫設計文件 |
| `IMPLEMENTATION_SUMMARY.md` | 完整實施總結 |
| `backend/.env` | 環境變數配置 |
| `backend/init_db.py` | 資料庫初始化腳本 |
| `frontend/src/pages/SingleInspectionPage.tsx` | 單片檢測頁面 |

---

## 🔥 立即開始

```bash
# 終端機 1 - 後端
cd aoi-system\backend
venv\Scripts\activate
python run.py

# 終端機 2 - 前端
cd aoi-system\frontend
npm run dev
```

開啟瀏覽器訪問: `http://localhost:5173`

---

## 📞 需要協助？

1. 查看詳細設定指南: `backend/SETUP_GUIDE.md`
2. 查看實施總結: `IMPLEMENTATION_SUMMARY.md`
3. 查看API文件: 後端啟動後訪問 `/api/health`

---

## 🎉 下一步

主題1已完成！您可以選擇繼續開發：

1. **主題5**: 批量載入儲存所有序號（推薦，與主題1相容性高）
2. **主題2**: B面檢測完畢自動合併產生雙面工單
3. **主題3**: 人工覆判

祝開發順利！🚀
