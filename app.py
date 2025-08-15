from flask import Flask, render_template, request, session
from dotenv import load_dotenv
import os
from uuid import uuid4

# LangChain 0.3.x
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore

from src.prompt import system_prompt
from src.helper import (
    download_hugging_face_embeddings,
    serper_search,
    format_serper_snippets,
)
from src.ncbi import fetch_ncbi_info  # <-- NCBI integration

# ------------ Flask & env ------------
app = Flask(__name__)
load_dotenv()
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-me")

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "")
HF_TOKEN = os.environ.get("HF_TOKEN", "")
SERPER_API_KEY = os.environ.get("SERPER_API_KEY", "")

# ------------ Embeddings / Retriever ------------
embeddings = download_hugging_face_embeddings()
INDEX_NAME = "medical-chatbot"
docsearch = PineconeVectorStore.from_existing_index(
    index_name=INDEX_NAME,
    embedding=embeddings
)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# ------------ LLM (Hugging Face OpenAI-compatible) ------------
llm = ChatOpenAI(
    api_key=HF_TOKEN,
    base_url="https://router.huggingface.co/v1",
    model="openai/gpt-oss-120b:novita",
    temperature=0.7,
    max_tokens=700,
)

# ------------ Prompt (now includes NCBI) ------------
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt + "\nUse the provided context and web results if helpful."),
        MessagesPlaceholder(variable_name="history"),
        ("human",
         "Question:\n{input}\n\n"
         "Retrieved Context:\n{context}\n\n"
         "NCBI PubMed:\n{ncbi_info}\n\n"
         "Web Results (Serper):\n{web_snips}"
        ),
    ]
)

chain = prompt | llm

# ------------ Memory per browser session ------------
_history_store = {}  # session_id -> InMemoryChatMessageHistory

def _get_session_id() -> str:
    if "sid" not in session:
        session["sid"] = str(uuid4())
    return session["sid"]

def _get_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in _history_store:
        _history_store[session_id] = InMemoryChatMessageHistory()
    return _history_store[session_id]

memory_chain = RunnableWithMessageHistory(
    chain,
    lambda sid: _get_history(sid),
    input_messages_key="input",
    history_messages_key="history",
)

# ------------ Routes ------------
@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/get", methods=["GET", "POST"])
def chat():
    user_msg = request.form["msg"]

    # Pinecone retrieval
    docs = retriever.get_relevant_documents(user_msg)
    context = "\n\n".join(doc.page_content for doc in docs) if docs else ""

    # NCBI PubMed (short hit)
    ncbi_info = fetch_ncbi_info(user_msg)

    # Serper (safe no-op if key missing inside your helper)
    web_data = serper_search(user_msg, num=5, gl="de", hl="en")
    web_snips = format_serper_snippets(web_data, limit=5)

    # Call LLM with memory
    sid = _get_session_id()
    ai_msg = memory_chain.invoke(
        {"input": user_msg, "context": context, "ncbi_info": ncbi_info, "web_snips": web_snips},
        config={"configurable": {"session_id": sid}},
    )

    return ai_msg.content if hasattr(ai_msg, "content") else str(ai_msg)



if __name__ == "__main__":
    port = int(os.environ.get("PORT", "7860"))  
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
