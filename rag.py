import streamlit as st
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import os
import uuid
import io
import google.generativeai as genai

# ========== CONFIGURATION ==========
QDRANT_URL = "https://2ed85abb-e606-4167-8d2e-ce4185f33997.us-east4-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.UYr-iYmbfZzhyr-lGQBlMlMuYQIAxriQhZd6af7vLq4"
COLLECTION_NAME = "rag_chat_app"

GEMINI_API_KEY = "AIzaSyBPpxPBZbbBJdfVTowZNzHa0AOwWwxMCgk"
genai.configure(api_key=GEMINI_API_KEY)

EMBED_MODEL = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

# ========== CREATE COLLECTION IF NOT EXISTS ==========
if not client.collection_exists(COLLECTION_NAME):
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=768, distance=Distance.COSINE)
    )

# ========== HELPERS ==========
def extract_text(file):
    ext = os.path.splitext(file.name)[-1].lower()
    if ext == '.pdf':
        reader = PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif ext == '.docx':
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    elif ext == '.txt':
        return file.read().decode("utf-8")
    else:
        raise ValueError(f"Unsupported file type: {ext}")

def embed_and_store(file, content):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(content)
    points = []
    for chunk in chunks:
        vector = EMBED_MODEL.encode(chunk)
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=vector.tolist(),
            payload={"source": file.name, "text": chunk}
        ))
    client.upsert(collection_name=COLLECTION_NAME, points=points)
    return len(chunks)

def search_context(query, top_k=3):
    query_vector = EMBED_MODEL.encode(query).tolist()
    results = client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True
    )
    return [res.payload["text"] for res in results]

def ask_gemini(prompt, context):
    full_prompt = f"""
You are an intelligent document assistant. Use the provided context to answer the user's question.

Question:
{prompt}

Context:
{context}

Answer based only on the context provided.
"""
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(full_prompt)
    return response.text.strip()

# ========== UI ==========
st.set_page_config(page_title="📚 Multi-Doc Chat (RAG)", layout="wide")
st.title("📚 Upload & Chat with Your Documents")

# --- Initialize session state for chat history ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Upload Multiple Files ---
uploaded_files = st.file_uploader("Upload PDF, DOCX, TXT files", type=["pdf", "docx", "txt"], accept_multiple_files=True)

if uploaded_files:
    with st.spinner("Processing and storing documents..."):
        total_chunks = 0
        for file in uploaded_files:
            try:
                text = extract_text(file)
                chunk_count = embed_and_store(file, text)
                total_chunks += chunk_count
            except Exception as e:
                st.error(f"Error processing {file.name}: {e}")
        st.success(f"✅ Successfully stored {total_chunks} chunks from {len(uploaded_files)} documents.")

# --- Chat Interface ---
st.divider()
st.subheader("💬 Ask a Question About Your Documents")

query = st.text_input("Type your question here...")

if query:
    try:
        with st.spinner("🔍 Searching relevant info..."):
            context_chunks = search_context(query, top_k=3)
            context = "\n".join(context_chunks)

        with st.spinner("🤖 Generating answer..."):
            answer = ask_gemini(query, context)

        st.markdown("### 🧠 Answer:")
        st.write(answer)

        # --- Append current interaction to chat history ---
        st.session_state.chat_history.append({
            "question": query,
            "answer": answer
        })

        # --- Generate combined chat history text ---
        history_text = ""
        for i, chat in enumerate(st.session_state.chat_history, start=1):
            history_text += f"Q{i}: {chat['question']}\nA{i}: {chat['answer']}\n\n"

        # --- Download chat history as TXT ---
        txt_bytes = io.BytesIO()
        txt_bytes.write(history_text.encode("utf-8"))
        txt_bytes.seek(0)
        st.download_button(
            label="📄 Download Chat History as TXT",
            data=txt_bytes,
            file_name="chat_history.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")
