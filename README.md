
# 📚 Multi-Document Chat with RAG (Retrieval-Augmented Generation)

This project is a **Streamlit application** that enables users to **upload and chat with multiple documents** (PDF, DOCX, TXT). It uses **Qdrant as the vector store**, **Sentence Transformers for embedding**, and **Gemini API (Generative AI)** to generate contextual answers based on user queries.

---

## 🚀 Features

* 📂 Upload multiple files (PDF, DOCX, TXT)
* 📄 Extract and chunk document text using LangChain's text splitter
* 🧠 Generate embeddings using Sentence Transformers (`all-MiniLM-L6-v2`)
* 📦 Store and retrieve embeddings with **Qdrant vector database**
* 🤖 Generate contextual answers using **Google Gemini 1.5 Flash**
* 🔎 Perform semantic search over your documents
* 💬 Clean, interactive chat interface powered by Streamlit

---

## 🛠️ Tech Stack

| Layer           | Tool / Library                                            |
| --------------- | --------------------------------------------------------- |
| Frontend        | Streamlit                                                 |
| Embedding Model | `sentence-transformers/all-MiniLM-L6-v2`                  |
| Vector DB       | Qdrant (Cloud Hosted)                                     |
| LLM             | Google Gemini 1.5 Flash (Generative AI)                   |
| File Handling   | `PyPDF2`, `python-docx`, native `.txt` parsing            |
| Chunking        | `langchain_text_splitters.RecursiveCharacterTextSplitter` |

---

## 📂 Project Structure

```
├── app.py                      # Main Streamlit app
├── requirements.txt            # Python dependencies
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/multi-doc-chat-rag.git
cd multi-doc-chat-rag
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt` example:**

```txt
streamlit
qdrant-client
sentence-transformers
PyPDF2
python-docx
langchain
google-generativeai
```

### 3. Configure API Keys

In `app.py`, replace the following values with your own:

```python
QDRANT_URL = "https://<your-qdrant-cluster>.cloud.qdrant.io"
QDRANT_API_KEY = "<your-qdrant-api-key>"

GEMINI_API_KEY = "<your-gemini-api-key>"
```

### 4. Run the App

```bash
streamlit run app.py
```

---

## 📌 Usage

1. Upload one or more documents (`.pdf`, `.docx`, `.txt`)
2. The app extracts, chunks, and embeds the document content.
3. Ask questions in natural language.
4. The app searches semantically relevant chunks and feeds them to Gemini.
5. Get accurate answers grounded in your documents.

---


## 📈 Future Enhancements

* 🔍 Highlight referenced context in UI
* 🧾 Add metadata filtering and document-level filtering
* 🌐 Support for other file types (e.g., XLSX)
* 🗂️ Persistent storage and user sessions

---

## 🧑‍💻 Author

**Yuva Sri Ramesh**
[Portfolio](https://yuva-sri-ramesh-portfolio.vercel.app) | [LinkedIn](https://www.linkedin.com/in/yuva-sri-ramesh/) | [GitHub](https://github.com/Yuva-Sri-Ramesh)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).


