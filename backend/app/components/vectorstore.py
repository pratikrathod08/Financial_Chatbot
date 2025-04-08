import os, sys
from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import numpy as np
import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import FakeEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class VectorStore:
    def __init__(self):
        self.index_path = "faiss_index"
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        self.embeddings = FakeEmbeddings(size=1352)

    def add_to_vectorstore(self, text: str, collection_name: str):
        docs = self.text_splitter.split_text(text)
        doc_objs = [Document(page_content=d, metadata={"collection": collection_name}) for d in docs]
        vector_store = FAISS.from_documents(doc_objs, self.embeddings)
        vector_store.save_local(self.index_path)
        return True

    def load_vectorstore(self):
        vector_store = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
        return vector_store

    def search_similar(self, query: str, top_k=3):
        vectorstore=self.load_vectorstore()
        results = vectorstore.similarity_search(query, k=top_k)
        return results

