import os
import uuid
import streamlit as st

from config.settings import UPLOAD_DIR
from services.document_service import extract_text
from services.vector_service import create_vector_db, search_relevant_chunks
from services.llm_service import ask_llm
from services.chat_service import (
    load_chat,
    save_chat,
    delete_chat,
    get_all_chats
)

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Smart Document Chatbot",
    page_icon="🤖",
    layout="wide"
)

# ---------------- DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background: #f8fafc;
}

.main-card {
    background: white;
    border: 1px solid #e5e7eb;
    padding: 24px;
    border-radius: 20px;
    margin-bottom: 20px;
}

.chat-user {
    background: #2563eb;
    color: white;
    padding: 14px 16px;
    border-radius: 16px 16px 4px 16px;
    margin: 10px 0 10px auto;
    max-width: 75%;
}

.chat-bot {
    background: #f1f5f9;
    color: #111827;
    padding: 14px 16px;
    border-radius: 16px 16px 16px 4px;
    margin: 10px auto 10px 0;
    max-width: 75%;
    border: 1px solid #e5e7eb;
}

.small-text {
    color: #64748b;
    font-size: 15px;
}

.sidebar-title {
    font-size: 24px;
    font-weight: 700;
}
.st-emotion-cache-1wjhcpo p {
    margin: -13px -5px;}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------

if "chat_id" not in st.session_state:
    st.session_state.chat_id = str(uuid.uuid4())

if "uploaded_file_key" not in st.session_state:
    st.session_state.uploaded_file_key = None

chat_data = load_chat(st.session_state.chat_id)

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown('<div class="sidebar-title">🤖 Smart Chatbot</div>', unsafe_allow_html=True)
    st.caption("Chat with PDF and Word documents")

    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.chat_id = str(uuid.uuid4())
        st.session_state.uploaded_file_key = None

        save_chat(st.session_state.chat_id, {
            "title": "New Chat",
            "collection": None,
            "messages": []
        })

        st.rerun()

    st.divider()
    st.subheader("💬 Saved Chats")

    chats = get_all_chats()

    if not chats:
        st.caption("No saved chats yet.")

    for cid, title in chats:
        col1, col2 = st.columns([4, 1])

        with col1:
            if st.button(title, key=f"open_{cid}", use_container_width=True):
                st.session_state.chat_id = cid
                st.session_state.uploaded_file_key = None
                st.rerun()

        with col2:
            if st.button("❌", key=f"delete_{cid}"):
                delete_chat(cid)

                if st.session_state.chat_id == cid:
                    st.session_state.chat_id = str(uuid.uuid4())
                    save_chat(st.session_state.chat_id, {
                        "title": "New Chat",
                        "collection": None,
                        "messages": []
                    })

                st.rerun()

# ---------------- MAIN UI ----------------

st.title("📄 Smart Document Chatbot")
st.markdown(
    '<p class="small-text">Upload a PDF or Word document, then ask questions from it.</p>',
    unsafe_allow_html=True
)

# ---------------- UPLOAD AREA ----------------

st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.subheader("📂 Upload Document")
st.write("Supported formats: **PDF (.pdf)** and **Word Document (.docx)**")

uploaded_file = st.file_uploader(
    "Choose your document",
    type=["pdf", "docx"],
    help="Only PDF and Word .docx files are supported."
)

if uploaded_file is not None:
    file_key = f"{uploaded_file.name}_{uploaded_file.size}"

    if st.session_state.uploaded_file_key != file_key:
        st.info("Please wait, your file is uploading and being indexed...")

        progress = st.progress(0)

        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        progress.progress(30)

        text = extract_text(file_path, uploaded_file.name)

        progress.progress(60)

        if text.strip():
            collection_name = create_vector_db(text, st.session_state.chat_id)

            if collection_name:
                chat_data = {
                    "title": uploaded_file.name,
                    "collection": collection_name,
                    "messages": []
                }

                save_chat(st.session_state.chat_id, chat_data)

                st.session_state.uploaded_file_key = file_key

                progress.progress(100)
                st.success("File uploaded successfully. You can start chatting now.")
                st.rerun()
            else:
                st.error("Could not create document index.")
        else:
            st.error("Could not extract text from this file.")
    else:
        st.success("File uploaded successfully. You can start chatting now.")

st.markdown("</div>", unsafe_allow_html=True)

# Reload latest chat data
chat_data = load_chat(st.session_state.chat_id)

# ---------------- CHAT AREA ----------------

st.markdown('<div class="main-card">', unsafe_allow_html=True)

st.subheader("💬 Chat")

if not chat_data.get("collection"):
    st.info("Upload a PDF or Word document first to start chatting.")
else:
    st.success("Document is ready. Ask your question below.")

for message in chat_data["messages"]:
    if message["role"] == "user":
        st.markdown(
            f'<div class="chat-user">🧑 {message["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-bot">🤖 {message["content"]}</div>',
            unsafe_allow_html=True
        )

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- CHAT INPUT ----------------

if chat_data.get("collection"):
    question = st.chat_input("Ask something about your uploaded document...")
else:
    question = st.chat_input("Upload a document first...", disabled=True)

if question:
    chat_data = load_chat(st.session_state.chat_id)

    chat_data["messages"].append({
        "role": "user",
        "content": question
    })

    with st.spinner("Thinking..."):
        try:
            chunks = search_relevant_chunks(
                chat_data["collection"],
                question,
                n_results=5
            )

            context = "\n\n---\n\n".join(chunks)
            answer = ask_llm(question, context)

        except Exception as e:
            answer = f"Error: {e}"

    chat_data["messages"].append({
        "role": "assistant",
        "content": answer
    })

    save_chat(st.session_state.chat_id, chat_data)
    st.rerun()