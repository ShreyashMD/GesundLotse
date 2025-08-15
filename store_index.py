from dotenv import load_dotenv
import os
from src.helper import (
    load_pdf_file,
    load_json_file,
    load_txt_file,
    filter_to_minimal_docs,
    text_split,
    download_hugging_face_embeddings,
)
from pinecone import Pinecone
from pinecone import ServerlessSpec
from langchain_pinecone import PineconeVectorStore

load_dotenv()

PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

def load_documents_from_data_folder(folder_path="data/"):
    documents = []
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        # Load depending on file extension
        if filename.lower().endswith(".pdf"):
            # load_pdf_file handles single files or directories (modify your helper accordingly)
            documents.extend(load_pdf_file(filepath))
        elif filename.lower().endswith(".json"):
            documents.extend(load_json_file(filepath))
        elif filename.lower().endswith(".txt"):
            documents.extend(load_txt_file(filepath))
    return documents

if __name__ == "__main__":
    # Load all supported documents from the data folder
    extracted_data = load_documents_from_data_folder()

    # Filter documents and split into chunks
    filter_data = filter_to_minimal_docs(extracted_data)
    text_chunks = text_split(filter_data)

    # Download embeddings model
    embeddings = download_hugging_face_embeddings()

    # Initialize Pinecone client
    pc = Pinecone(api_key=PINECONE_API_KEY)
    index_name = "medical-chatbot"  # change if desired

    # Create index if it doesn't exist
    if not pc.has_index(index_name):
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

    # Get the index object
    index = pc.Index(index_name)

    # Create the Pinecone vector store from documents
    docsearch = PineconeVectorStore.from_documents(
        documents=text_chunks,
        index_name=index_name,
        embedding=embeddings,
    )

    print(f"Index '{index_name}' populated with {len(text_chunks)} document chunks.")
