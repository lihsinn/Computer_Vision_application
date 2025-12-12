# 快速启动指南 (Quick Start Guide)

## Windows 用户

### 方法 1: 使用启动脚本（推荐）

1. **启动后端**
   - 双击 `start-backend.bat`
   - 等待服务器启动，看到 "Running on http://0.0.0.0:5000" 信息

2. **启动前端**
   - 双击 `start-frontend.bat`
   - 等待服务器启动，浏览器会自动打开

3. **开始使用**
   - 访问 http://localhost:5173
   - 上传图像并开始检测！

### 方法 2: 手动启动

#### 启动后端:
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

#### 启动前端:
```bash
cd frontend
npm install
npm run dev
```

---

## macOS/Linux 用户

### 启动后端:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

### 启动前端:
```bash
cd frontend
npm install
npm run dev
```

---

## 验证安装

### 检查后端:
访问 http://localhost:5000/api/health

应该看到:
```json
{
  "status": "healthy",
  "message": "AOI Backend is running"
}
```

### 检查前端:
访问 http://localhost:5173

应该看到 AOI 系统的主界面

---

## 常见问题

### Python 命令不存在
- 尝试使用 `python3` 代替 `python`
- 确认已安装 Python 3.8+

### npm 命令不存在
- 安装 Node.js: https://nodejs.org/
- 重启终端

### 端口被占用
- 后端: 修改 `backend/run.py` 中的端口号
- 前端: 修改 `frontend/vite.config.ts` 中的端口号

### 虚拟环境激活失败
- Windows: 以管理员身份运行终端
- 或使用: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## 下一步

查看完整文档: [README.md](./README.md)

开始使用系统进行 AOI 检测！

**祝使用愉快！ 🚀**
