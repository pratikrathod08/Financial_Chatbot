import os, sys
from PyPDF2 import PdfReader
import numpy as np
import faiss
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.database.database import get_full_schema
from app.config import ROOT_DIR
from app.logger import logger
from app.exception import CustomException

from dotenv import load_dotenv

load_dotenv()

class VectorStore:
    def __init__(self):
        try: 
            logger.info("Vector store initialized.")
            self.index_path = os.path.join(ROOT_DIR,"faiss_index")
            self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
            self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2") 
        except Exception as e: 
            logger.info(f"Exception occure during vector initialize: {str(e)}")
            raise CustomException(e, sys) 

    def add_to_vectorstore(self, text: str, collection_name: str):
        try: 
            logger.info("Vector store data ingestion started")
            docs = self.text_splitter.split_text(text)
            if not docs:
                logger.warning(f"Text splitter returned empty chunks for file: {collection_name}")
                return False
            doc_objs = [Document(page_content=d, metadata={"collection": collection_name}) for d in docs]
            vector_store = FAISS.from_documents(doc_objs, self.embeddings)
            vector_store.save_local(self.index_path)
            logger.info("Vectore stored completed")
            return True
        except Exception as e: 
            logger.info(f"Exception occure during add data to vectorstore: {str(e)}")
            raise CustomException(e, sys) 

    def load_vectorstore(self):
        try: 
            logger.info("Vector loading started")
            vector_store = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
            logger.info("Vectore loaded completed")
            return vector_store
        except Exception as e: 
            logger.info(f"Exception occure during load vectorstore: {str(e)}")
            raise CustomException(e, sys) 

    @tool
    def search_similar(self, query: str, top_k=3):
        """ Similarity search tool using vector database """
        try:
            vectorstore=self.load_vectorstore()
            results = vectorstore.similarity_search(query, k=top_k)
            logger.info("Similarity search done : ")
            logger.info(results)
            return "\n\n".join([doc.page_content for doc in results])
        except Exception as e:
            logger.info("Exception occure during search similarity : {str(e)}")
            raise CustomException(e, sys)
            



