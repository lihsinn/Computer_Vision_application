# AOI System 後端設定指南

## 📋 前置需求

1. **Python 3.8+**
2. **PostgreSQL 12+**
3. **pip** (Python套件管理器)

---

## 🗄️ 資料庫設定

### 步驟 1: 安裝 PostgreSQL

#### Windows:
1. 下載 PostgreSQL: https://www.postgresql.org/download/windows/
2. 執行安裝程式
3. 預設埠號: `5432`
4. 設定密碼（例如: `postgres`）

#### macOS:
```bash
brew install postgresql@14
brew services start postgresql@14
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### 步驟 2: 建立資料庫

打開 PostgreSQL 命令列工具 (psql)：

```sql
-- 建立資料庫
CREATE DATABASE aoi_system;

-- 建立使用者（選用）
CREATE USER aoi_user WITH PASSWORD 'your_password';

-- 授予權限
GRANT ALL PRIVILEGES ON DATABASE aoi_system TO aoi_user;

-- 查看資料庫
\l
```

---

## 🐍 Python 環境設定

### 步驟 1: 建立虛擬環境

```bash
cd aoi-system/backend

# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 步驟 2: 安裝依賴套件

```bash
pip install -r requirements.txt
```

### 步驟 3: 配置環境變數

複製 `.env.example` 為 `.env`：

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

編輯 `.env` 檔案：

```env
# 資料庫配置
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/aoi_system

# Flask配置
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
```

**重要**: 修改 `DATABASE_URL` 以符合您的資料庫設定：
- `postgres:postgres` → 您的使用者名稱:密碼
- `localhost:5432` → 資料庫主機:埠號
- `aoi_system` → 資料庫名稱

---

## 🏗️ 初始化資料庫

### 步驟 1: 測試資料庫連接

```bash
python -c "from app.database import engine; engine.connect(); print('✅ 資料庫連接成功!')"
```

### 步驟 2: 建立資料表

```bash
python init_db.py --create
```

您應該會看到以下輸出：
```
🚀 正在建立資料庫表格...
✅ 資料庫表格建立成功！

已建立的表格:
  - lots
  - inspections
  - cells
  - defects
  - manual_reviews
  - merged_inspections
  - marking_card_params
```

### 其他資料庫操作

```bash
# 刪除所有表格 (危險！)
python init_db.py --drop

# 重置資料庫 (刪除後重建)
python init_db.py --reset
```

---

## 🚀 啟動後端伺服器

### 方法 1: 使用批次檔 (Windows)

```bash
start-backend.bat
```

### 方法 2: 使用 Python

```bash
# 啟動 Flask 開發伺服器
python run.py
```

伺服器將在 `http://0.0.0.0:5000` 啟動

### 驗證伺服器運行

訪問健康檢查端點：
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

---

## 🧪 測試 API

### 使用 curl 測試

#### 1. 建立批次

```bash
curl -X POST http://localhost:5000/api/lots \
  -H "Content-Type: application/json" \
  -d "{\"lot_number\": \"LOT001\", \"description\": \"測試批次\"}"
```

#### 2. 取得批次列表

```bash
curl http://localhost:5000/api/lots
```

#### 3. 建立檢測記錄

```bash
curl -X POST http://localhost:5000/api/inspections \
  -H "Content-Type: application/json" \
  -d "{
    \"lot_id\": \"<your-lot-id>\",
    \"serial_number\": \"001\",
    \"side\": \"A\",
    \"inspection_mode\": \"OfflineTest\",
    \"inspection_type\": \"SingleInsp\",
    \"image_path\": \"/temp/test.jpg\",
    \"cells\": [
      {
        \"cell_number\": 1,
        \"position_x\": 100,
        \"position_y\": 100,
        \"width\": 50,
        \"height\": 50,
        \"status\": \"PASS\"
      }
    ],
    \"defects\": {}
  }"
```

---

## 📂 專案結構

```
backend/
├── app/
│   ├── __init__.py           # Flask應用工廠
│   ├── database.py           # 資料庫配置
│   ├── models/               # 資料庫模型
│   │   ├── lot.py
│   │   ├── inspection.py
│   │   ├── cell.py
│   │   └── ...
│   ├── routes/               # API路由
│   │   ├── upload.py
│   │   ├── process.py
│   │   └── inspection.py
│   └── services/             # 業務邏輯
│       ├── aoi_service.py
│       └── image_handler.py
├── temp/                     # 暫存檔案
├── .env                      # 環境變數
├── requirements.txt          # Python依賴
├── init_db.py               # 資料庫初始化腳本
└── run.py                   # 應用啟動入口
```

---

## 🔧 常見問題

### 問題 1: 無法連接資料庫

**錯誤訊息**: `could not connect to server`

**解決方案**:
1. 確認 PostgreSQL 服務正在運行
   ```bash
   # Windows
   services.msc (查找 postgresql-x64-14)

   # macOS
   brew services list

   # Linux
   sudo systemctl status postgresql
   ```

2. 檢查 `.env` 中的 `DATABASE_URL` 是否正確

3. 測試資料庫連接：
   ```bash
   psql -h localhost -U postgres -d aoi_system
   ```

### 問題 2: 缺少 psycopg2

**錯誤訊息**: `No module named 'psycopg2'`

**解決方案**:
```bash
pip install psycopg2-binary
```

### 問題 3: 權限錯誤

**錯誤訊息**: `permission denied for database`

**解決方案**:
在 psql 中執行：
```sql
GRANT ALL PRIVILEGES ON DATABASE aoi_system TO your_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
```

### 問題 4: 埠號已被佔用

**錯誤訊息**: `Address already in use: 5000`

**解決方案**:
修改 `run.py` 中的埠號：
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

---

## 📚 API 文件

### 批次管理

| 端點 | 方法 | 說明 |
|------|------|------|
| `/api/lots` | POST | 建立新批次 |
| `/api/lots` | GET | 取得批次列表 |
| `/api/lots/<id>` | GET | 取得批次詳情 |

### 檢測記錄

| 端點 | 方法 | 說明 |
|------|------|------|
| `/api/inspections` | POST | 建立檢測記錄 |
| `/api/inspections` | GET | 取得檢測列表 |
| `/api/inspections/<id>` | GET | 取得檢測詳情 |
| `/api/inspections/<id>/cells` | GET | 取得Cell列表 |

### 影像處理

| 端點 | 方法 | 說明 |
|------|------|------|
| `/api/upload` | POST | 上傳影像 |
| `/api/process/defect-detection` | POST | 瑕疵檢測 |
| `/api/process/measurement` | POST | 尺寸測量 |

---

## 🎯 下一步

1. **安裝前端**: 參考 `frontend/README.md`
2. **測試系統**: 執行完整的檢測流程
3. **開發新功能**: 參考 `database_design.md`

---

## 📞 支援

如有問題，請參考：
- 資料庫設計文件: `database_design.md`
- 專案摘要: `PROJECT_SUMMARY.md`
