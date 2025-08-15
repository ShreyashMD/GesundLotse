import os
import json
from typing import List
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_pdf_file(path) -> List[Document]:
    # Accept either a directory or a single PDF file
    if os.path.isdir(path):
        loader = DirectoryLoader(path, glob="*.pdf", loader_cls=PyPDFLoader)
        documents = loader.load()
    else:
        loader = PyPDFLoader(path)
        documents = loader.load()
    return documents

def load_json_file(filepath) -> List[Document]:
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    documents = []
    if isinstance(data, list):
        for entry in data:
            text = entry.get('content', '')  # adjust key if needed
            if text:
                documents.append(Document(page_content=text, metadata={"source": filepath}))
    else:
        text = data.get('content', '')
        if text:
            documents.append(Document(page_content=text, metadata={"source": filepath}))
    return documents

def load_txt_file(filepath) -> List[Document]:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    return [Document(page_content=text, metadata={"source": filepath})]

def filter_to_minimal_docs(docs: List[Document]) -> List[Document]:
    minimal_docs = []
    for doc in docs:
        src = doc.metadata.get("source")
        minimal_docs.append(
            Document(
                page_content=doc.page_content,
                metadata={"source": src}
            )
        )
    return minimal_docs

def text_split(extracted_data: List[Document]) -> List[Document]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    text_chunks = text_splitter.split_documents(extracted_data)
    return text_chunks

def download_hugging_face_embeddings():
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')  # 384 dims
    return embeddings


SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")

def serper_search(query: str, num: int = 5, gl: str = "de", hl: str = "en") -> dict:
    """
    Returns Serper JSON or {} on failure. Uses env SERPER_API_KEY.
    """
    if not SERPER_API_KEY:
        return {}
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "num": num, "gl": gl, "hl": hl, "autocorrect": True}
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception:
        return {}

def format_serper_snippets(data: dict, limit: int = 5) -> str:
    """
    Turn top organic results into short bullet snippets.
    """
    if not data:
        return ""
    lines = []
    for item in (data.get("organic") or [])[:limit]:
        title = (item.get("title") or "").strip()
        snippet = (item.get("snippet") or "").strip()
        source = (item.get("link") or "").strip()
        if title or snippet:
            lines.append(f"- {title}: {snippet}\n  Source: {source}")
    return "\n".join(lines)