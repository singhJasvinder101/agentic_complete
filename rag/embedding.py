from dotenv import load_dotenv
import os
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

script_dir = Path(__file__).parent
pdf_path = script_dir / "nodejs.pdf"

loader = PyPDFLoader(str(pdf_path))

# gives every single page
docs = loader.load()

print(docs[0])

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(documents=docs)

print(chunks[0])
print(chunks[1])

embedding_model = OpenAIEmbeddings(
    model = "text-embedding-3-large",
)


vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="rag-collection-nodejs"
)

print("Indexing done")