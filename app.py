import streamlit as st
import requests
import os
import traceback

st.set_page_config(page_title="RAG 私有知识库对话机器人", page_icon="📚", layout="wide")

# Streamlit Cloud部署配置
# 后端API地址 - Streamlit Cloud上需要使用外部可访问的API服务
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8003")

st.title("📚 基于 RAG+LangChain 的私有知识库对话机器人")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents_uploaded" not in st.session_state:
    st.session_state.documents_uploaded = False

def check_backend_connection():
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except Exception as e:
        return False

with st.sidebar:
    st.header("📁 上传文档")

    backend_status = check_backend_connection()
    if backend_status:
        st.success("✅ 后端服务已连接")
    else:
        st.error("❌ 无法连接后端服务")
        st.info("💡 请确保后端API服务正在运行")
        st.info(f"📌 当前API地址: {BACKEND_URL}")

    uploaded_files = st.file_uploader(
        "选择 PDF/TXT/MD 文件",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True
    )

    if st.button("上传并处理文档"):
        if not uploaded_files:
            st.warning("⚠️ 请先选择文件")
        elif not backend_status:
            st.error("❌ 后端服务未连接，请检查后端是否运行")
        else:
            with st.spinner("正在处理文档..."):
                try:
                    files = []
                    for file in uploaded_files:
                        file_ext = file.name.split(".")[-1].lower()
                        if file_ext == "txt":
                            files.append(("files", (file.name, file.getvalue(), "text/plain")))
                        else:
                            files.append(("files", (file.name, file, file.type)))

                    st.info(f"📤 正在上传 {len(files)} 个文件...")
                    response = requests.post(f"{BACKEND_URL}/upload_documents", files=files, timeout=30)
                    st.info(f"📥 响应状态: {response.status_code}")

                    if response.status_code == 200:
                        result = response.json()
                        st.success(f"✅ 文档处理成功！{result['message']}")
                        st.session_state.documents_uploaded = True
                    else:
                        st.error(f"❌ 上传失败 (状态码: {response.status_code}): {response.text}")

                except requests.exceptions.ConnectionError:
                    st.error("❌ 连接失败：无法连接到后端服务")
                except requests.exceptions.Timeout:
                    st.error("❌ 请求超时：后端服务响应过慢")
                except Exception as e:
                    st.error(f"❌ 发生错误: {str(e)}")
                    st.error(f"详细信息: {traceback.format_exc()}")

    if st.button("清空对话历史"):
        try:
            response = requests.post(f"{BACKEND_URL}/clear_memory")
            if response.status_code == 200:
                st.session_state.messages = []
                st.success("✅ 对话历史已清空")
        except Exception as e:
            st.error(f"❌ 操作失败: {str(e)}")

    st.markdown("---")
    st.info("支持格式: PDF、TXT、Markdown")
    st.info("后端服务: FastAPI + DeepSeek")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("请输入您的问题..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI 正在思考..."):
            try:
                response = requests.post(f"{BACKEND_URL}/query", json={"question": prompt}, timeout=60)
                if response.status_code == 200:
                    result = response.json()
                    answer = result.get("answer", "暂无回答")
                    st.markdown(answer)

                    sources = result.get("sources", [])
                    if sources:
                        with st.expander("📖 参考来源"):
                            for i, source in enumerate(sources, 1):
                                st.markdown(f"**来源 {i}:**")
                                st.markdown(source[:500] + "..." if len(source) > 500 else source)

                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    st.error(f"❌ 请求失败 (状态码: {response.status_code}): {response.text}")
            except requests.exceptions.ConnectionError:
                st.error("❌ 连接失败：无法连接到后端服务")
            except Exception as e:
                st.error(f"❌ 发生错误: {str(e)}")

if not st.session_state.documents_uploaded:
    st.warning("⚠️ 请先上传文档，否则 AI 将无法基于文档内容回答问题")