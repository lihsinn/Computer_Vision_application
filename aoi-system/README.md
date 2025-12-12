# AOI Inspection System
**Automated Optical Inspection System**
Web-based defect detection, measurement, and quality control

---

## 系统概述

这是一个完整的 AOI（自动光学检测）系统，基于 Web 技术栈构建，用于工业检测、品质控制和缺陷分析。

### 主要功能

- 🔍 **瑕疵检测**：基于模板比对的自动缺陷检测
- 📏 **尺寸测量**：精确的物体尺寸测量（支持像素到实际单位转换）
- 🎯 **定位标记检测**：自动识别 PCB/工件上的定位标记
- 📊 **可视化结果**：直观的检测结果展示和标注
- 📄 **报告生成**：详细的检测报告

### 技术栈

**前端:**
- React 18
- TypeScript
- Vite
- Axios

**后端:**
- Python 3.8+
- Flask 3.0
- OpenCV 4.8
- NumPy

---

## 项目结构

```
aoi-system/
├── backend/                    # Flask API 后端
│   ├── app/
│   │   ├── __init__.py        # Flask 应用工厂
│   │   ├── routes/            # API 路由
│   │   │   ├── upload.py      # 图像上传
│   │   │   └── process.py     # 图像处理
│   │   └── services/          # 业务逻辑
│   │       ├── aoi_service.py # CV 算法包装器
│   │       └── image_handler.py
│   ├── temp/                   # 临时文件存储
│   ├── requirements.txt
│   └── run.py                  # 入口文件
│
├── frontend/                   # React 前端
│   ├── src/
│   │   ├── components/        # React 组件
│   │   │   ├── ImageUpload.tsx
│   │   │   ├── ImageViewer.tsx
│   │   │   └── ResultsPanel.tsx
│   │   ├── services/
│   │   │   └── api.ts         # API 客户端
│   │   ├── types/
│   │   │   └── aoi.types.ts   # TypeScript 类型
│   │   ├── styles/            # CSS 样式
│   │   ├── App.tsx
│   │   └── main.tsx
│   └── package.json
│
└── README.md
```

---

## 快速开始

### 前置要求

- **Node.js**: 16+
- **Python**: 3.8+
- **pip**: 最新版本

### 1. 后端设置

#### 步骤 1: 创建 Python 虚拟环境

```bash
cd aoi-system/backend
python -m venv venv
```

#### 步骤 2: 激活虚拟环境

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

#### 步骤 3: 安装依赖

```bash
pip install -r requirements.txt
```

#### 步骤 4: 启动后端服务器

```bash
python run.py
```

后端将在 `http://localhost:5000` 运行

---

### 2. 前端设置

打开新的终端窗口：

#### 步骤 1: 进入前端目录

```bash
cd aoi-system/frontend
```

#### 步骤 2: 安装依赖 (如果还没安装)

```bash
npm install
```

#### 步骤 3: 启动开发服务器

```bash
npm run dev
```

前端将在 `http://localhost:5173` 运行

---

## 使用方法

### 1. 访问应用

在浏览器中打开: `http://localhost:5173`

### 2. 上传图像

- 点击上传区域或拖拽图像文件
- 支持格式：PNG, JPG, BMP, TIFF
- 最大文件大小：16MB

### 3. 选择处理模式

#### 瑕疵检测 (Defect Detection)
- 检测图像中的缺陷和异常
- 可调整阈值参数 (10-100)
- 显示缺陷位置、面积和边界框

#### 尺寸测量 (Measurement)
- 测量物体的宽度、高度、面积
- 设置校准系数（像素到毫米）
- 自动识别矩形和圆形

#### 定位标记检测 (Fiducial Marks)
- 检测圆形定位标记
- 计算旋转角度
- 可调整半径范围

### 4. 查看结果

- 左侧：原始图像与标注图像对比
- 右侧：详细的检测数据表格
- 可在不同结果类型间切换

---

## API 文档

### 基础 URL

```
http://localhost:5000/api
```

### 端点列表

#### 1. 健康检查

```http
GET /api/health
```

**响应:**
```json
{
  "status": "healthy",
  "message": "AOI Backend is running"
}
```

---

#### 2. 上传图像

```http
POST /api/upload
```

**请求:**
- Content-Type: `multipart/form-data`
- Body: `image` (文件)

**响应:**
```json
{
  "success": true,
  "image_id": "uuid-string",
  "filename": "test.jpg",
  "size": {
    "width": 800,
    "height": 600
  }
}
```

---

#### 3. 瑕疵检测

```http
POST /api/process/defect-detection
```

**请求 Body:**
```json
{
  "image_id": "uuid-string",
  "threshold": 30
}
```

**响应:**
```json
{
  "success": true,
  "defects": [
    {
      "id": 1,
      "position": { "x": 100, "y": 200 },
      "area": 150.5,
      "bbox": { "x": 95, "y": 195, "width": 20, "height": 25 }
    }
  ],
  "defect_count": 3,
  "annotated_image": "base64-encoded-image"
}
```

---

#### 4. 尺寸测量

```http
POST /api/process/measurement
```

**请求 Body:**
```json
{
  "image_id": "uuid-string",
  "calibration": { "pixel_to_mm": 0.1 }
}
```

**响应:**
```json
{
  "success": true,
  "measurements": [
    {
      "object_id": 1,
      "shape": "rectangle",
      "width_mm": 20.5,
      "height_mm": 15.3,
      "area_mm2": 313.65,
      "bbox": { "x": 100, "y": 100, "width": 205, "height": 153 }
    }
  ],
  "annotated_image": "base64-encoded-image"
}
```

---

#### 5. 定位标记检测

```http
POST /api/process/fiducial-detection
```

**请求 Body:**
```json
{
  "image_id": "uuid-string",
  "min_radius": 5,
  "max_radius": 25
}
```

**响应:**
```json
{
  "success": true,
  "marks": [
    {
      "id": 1,
      "position": { "x": 150, "y": 150 },
      "radius": 20
    }
  ],
  "rotation_angle": 15.5,
  "annotated_image": "base64-encoded-image"
}
```

---

## 开发说明

### 后端开发

1. **添加新的处理算法**
   - 在 `backend/app/services/aoi_service.py` 中添加新方法
   - 在 `backend/app/routes/process.py` 中创建新端点

2. **修改现有算法**
   - 编辑 `backend/app/services/aoi_service.py`
   - 参考 `practice/3_image_processing/` 中的原始 CV 代码

### 前端开发

1. **添加新组件**
   - 在 `frontend/src/components/` 创建新的 `.tsx` 文件
   - 在 `frontend/src/styles/` 创建对应的 `.css` 文件

2. **修改 API 调用**
   - 编辑 `frontend/src/services/api.ts`
   - 更新 `frontend/src/types/aoi.types.ts` 中的类型定义

---

## 常见问题

### Q: 后端启动失败

**A:** 检查以下内容：
1. 确认 Python 版本 >= 3.8
2. 确认虚拟环境已激活
3. 确认所有依赖已安装：`pip install -r requirements.txt`
4. 检查端口 5000 是否被占用

### Q: 前端无法连接后端

**A:**
1. 确认后端正在运行（访问 `http://localhost:5000/api/health`）
2. 检查 CORS 设置
3. 查看浏览器控制台的错误信息

### Q: 图像处理很慢

**A:**
1. 确保图像大小不超过 16MB
2. 考虑压缩图像尺寸
3. 调整处理参数（降低精度可提高速度）

### Q: 检测结果不准确

**A:**
1. 调整阈值参数
2. 使用高质量的参考模板
3. 确保图像光照均匀

---

## 未来改进

- [ ] PDF 报告生成
- [ ] 批量图像处理
- [ ] 用户认证系统
- [ ] 数据库持久化
- [ ] AI 深度学习检测
- [ ] 实时相机集成
- [ ] 历史记录查询
- [ ] 统计分析仪表板

---

## 贡献

欢迎提交 Issue 和 Pull Request！

---

## 许可证

MIT License

---

## 联系方式

如有问题或建议，请联系开发团队。

**Built with ❤️ using React, TypeScript, Flask, and OpenCV**
