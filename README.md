# RAG 私有知识库对话机器人

一个基于 RAG（检索增强生成）技术的智能问答系统，支持上传文档并基于文档内容进行智能问答。

## 功能特点

- 📄 支持上传 PDF、TXT、Markdown 文档
- 🤖 基于文档内容的智能问答
- 🔗 支持 DeepSeek API 进行答案生成
- 📚 文档分段和智能检索
- 💬 友好的 Web 界面

## 部署说明

### 1. 后端服务部署

本项目需要先部署后端 API 服务。后端服务地址需要设置为环境变量 `BACKEND_URL`。

后端服务应包含以下 API 端点：
- `GET /health` - 健康检查
- `POST /upload_documents` - 上传文档
- `POST /query` - 智能问答
- `POST /clear_memory` - 清空对话历史

### 2. Streamlit Cloud 部署

1. 将本文件夹内容推送到 GitHub 仓库
2. 访问 [Streamlit Cloud](https://streamlit.io/cloud)
3. 创建新应用并连接 GitHub 仓库
4. 设置环境变量 `BACKEND_URL` 为您的后端 API 地址
5. 部署应用

### 3. 环境变量配置

在 Streamlit Cloud 中需要设置以下环境变量：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| BACKEND_URL | 后端API服务地址 | https://your-api.herokuapp.com |

## 项目结构

```
streamlit_cloud/
├── app.py              # Streamlit 主应用
├── requirements.txt    # Python 依赖
└── README.md          # 说明文档
```

## 使用说明

1. 启动后端 API 服务
2. 访问 Streamlit Cloud 上的应用
3. 上传文档（PDF、TXT 或 Markdown）
4. 输入问题进行智能问答

## 技术栈

- **前端**: Streamlit
- **后端**: FastAPI
- **AI模型**: DeepSeek API
- **文档处理**: LangChain

## 许可证

MIT License