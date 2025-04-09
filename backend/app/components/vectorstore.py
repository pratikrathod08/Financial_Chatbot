import os, sys
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import numpy as np
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.logger import logger

class VectorStore:
    logger.info("Vector store started")

    def __init__(self):
        self.index_path = "faiss_index"
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")  # Or any other suitable model

    def add_to_vectorstore(self, text: str, collection_name: str):
        docs = self.text_splitter.split_text(text)
        doc_objs = [Document(page_content=d, metadata={"collection": collection_name}) for d in docs]
        vector_store = FAISS.from_documents(doc_objs, self.embeddings)
        vector_store.save_local(self.index_path)
        logger.info("Vectore stored completed")
        return True

    def load_vectorstore(self):
        vector_store = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
        logger.info("Vectore loaded completed")
        return vector_store

    def search_similar(self, query: str, top_k=3):
        try:
            vectorstore=self.load_vectorstore()
            results = vectorstore.similarity_search(query, k=top_k)
            logger.info("Similarity search done : ")
            logger.info(results)
            return results
        except Exception as e:
            return {"error": e}

