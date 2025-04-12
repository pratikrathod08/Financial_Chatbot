import os, sys
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools import tool
from app.config import ROOT_DIR
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pprint import pprint
load_dotenv()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
index_path = os.path.join(ROOT_DIR,"faiss_index")

def load_vectorstore():
    vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    return vector_store

def search_similar(query: str, top_k=4):
    try:
        vectorstore=load_vectorstore()
        results = vectorstore.similarity_search(query, k=top_k)
        print(results)
        return results
    except Exception as e:
        return {"error": e}

@tool
def lookup_vectordb(query: str)->str:
    """Search within the vectordb to check whether certain options are permitted. Input should be a search query."""
    vectordb = load_vectorstore()
    docs = vectordb.similarity_search(query)
    return "\n\n".join([doc.page_content for doc in docs])

# print(lookup_vectordb)