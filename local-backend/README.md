# Local Backend for Word Legal Assistant

本项目为Word法律助手的本地后端，支持知识库管理与OpenAI格式AI接口。

## 一键启动

```bash
cd local-backend
npm install
npm start
```

## 环境变量

- `OPENAI_API_KEY`：你的OpenAI API密钥（必填）
- `PORT`：服务端口（可选，默认3001）

可在启动前设置：
```bash
export OPENAI_API_KEY=你的key
export PORT=3001
```

## 目录结构

```
local-backend/
├── src/
│   ├── controllers/
│   ├── models/
│   ├── routes/
│   ├── services/
│   ├── utils/
│   └── app.js
├── templates/         # 存放模板文件
├── db.sqlite          # 元数据
├── package.json
├── README.md
└── start.sh
```

## API说明

### 模板管理
- `GET    /api/templates`         获取所有模板元数据
- `POST   /api/templates`         上传新模板（multipart/form-data）
- `GET    /api/templates/:id`     获取单个模板内容
- `DELETE /api/templates/:id`     删除模板

### AI接口
- `POST   /api/ai`                调用OpenAI格式AI接口

## 依赖
- Node.js 16+
- npm