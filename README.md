# Word Legal Assistant 本地部署与运行说明

本系统包含**本地后端服务**和**Word插件前端**，全部可在Windows电脑本地运行，无需云端依赖，保障数据隐私。

---

## 一、环境准备

1. **安装 [Node.js 16+](https://nodejs.org/zh-cn/download/)**
2. **安装 Office Add-in CLI 工具（用于开发和调试Word插件）**
   ```bash
   npm install -g yo generator-office
   ```
3. **准备 OpenAI API Key**  
   （如需AI功能，需注册OpenAI账号并获取API Key）

---

## 二、启动本地后端服务

1. 打开命令行（cmd/PowerShell），进入后端目录：
   ```bat
   cd local-backend
   ```
2. 设置环境变量（推荐在命令行中设置，或写入`.env`文件）：
   ```bat
   set OPENAI_API_KEY=你的key
   set PORT=3001
   ```
3. 一键启动（推荐）：
   ```bat
   start.bat
   ```
   或手动启动：
   ```bat
   npm install
   npm start
   ```
4. 启动成功后，后端服务监听在 `http://localhost:3001`，并自动创建本地知识库（templates/）和数据库（db.sqlite）。

---

## 三、启动Word插件前端

1. 打开新命令行窗口，进入前端目录：
   ```bat
   cd word-addin
   ```
2. 安装依赖：
   ```bat
   npm install
   ```
3. 启动开发服务器：
   ```bat
   npm start
   ```
   默认监听 `https://localhost:3000`。

---

## 四、在Word中加载插件

1. 打开**Windows版Word**（2016+ 或 Microsoft 365）
2. 选择“插入” > “我的加载项” > “共享文件夹”
3. 选择 `word-addin/public/manifest.xml` 文件
4. 插件将以侧边栏形式出现

---

## 五、主要功能

- **模板管理**：上传、浏览、插入本地知识库模板到Word文档
- **AI能力**：输入需求，AI起草/润色/审查，结果一键插入Word
- **全部本地运行**，保障数据隐私

---

## 六、常见问题与注意事项

- **后端端口冲突**：如3001端口被占用，可修改`PORT`环境变量
- **API Key未配置**：未设置`OPENAI_API_KEY`将无法使用AI功能
- **证书警告**：开发环境下前端为`https`，首次访问可能有证书警告，选择“继续访问”即可
- **Word加载项未显示**：请确保前端和后端都已启动，且manifest.xml路径正确
- **模板格式**：目前插入Word仅支持纯文本，上传docx/pdf等格式时插入内容为文本

---

## 七、目录结构说明

```
workspace/
├── local-backend/         # 后端服务
│   ├── src/
│   ├── templates/
│   ├── db.sqlite
│   ├── start.bat
│   └── ...
└── word-addin/            # Word插件前端
    ├── src/
    ├── public/
    │   └── manifest.xml
    └── ...
```

---

如需进一步定制、遇到问题或需要远程协助，请联系开发者或技术支持。
