# Word Legal Assistant Add-in

本项目为Word法律助手的前端插件，基于Office.js + React，支持在Windows本地Word中运行，并与本地后端通信。

## 开发环境准备

1. 安装 [Node.js 16+](https://nodejs.org/zh-cn/download/)
2. 安装 [Office Add-in CLI 工具](https://docs.microsoft.com/zh-cn/office/dev/add-ins/overview/office-add-ins)
   ```bash
   npm install -g yo generator-office
   ```
3. 安装依赖
   ```bash
   cd word-addin
   npm install
   ```

## 启动开发服务器

```bash
npm start
```

## 在Word中加载插件

1. 打开Word（Windows版，2016+ 或 Microsoft 365）
2. 选择“插入” > “我的加载项” > “共享文件夹”
3. 选择本项目中的 `manifest.xml`
4. 插件将以侧边栏形式出现

## 功能说明
- 显示和插入本地知识库模板
- 上传新模板
- AI起草/润色/审查（调用本地后端API）

## 注意事项
- 本插件通过 `http://localhost:3001` 访问本地后端服务，请确保后端已启动
- 推荐使用Edge或Chrome浏览器调试