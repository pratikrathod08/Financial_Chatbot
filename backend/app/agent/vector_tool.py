import os, sys
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.tools import tool

from app.config import ROOT_DIR
from app.logger import logger 
from app.exception import CustomException

from dotenv import load_dotenv
from pprint import pprint
load_dotenv()


text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
index_path = os.path.join(ROOT_DIR,"faiss_index")

def load_vectorstore():
    try: 
        logger.info("Load vector started")
        vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
        logger.info(f"Vector loaded successfully : {vector_store}")
        return vector_store
    except Exception as e:
        logger.info(f"Exception occure during load vector : {str(e)}")
        raise CustomException(e, sys)

def search_similar(query: str, top_k=4):
    try:
        logger.info("Similarity search started")
        vectorstore=load_vectorstore()
        results = vectorstore.similarity_search(query, k=top_k)
        logger.info(f"Similarity search result : {results}")
        return results
    except Exception as e:
        logger.info(f"Exception occure during similarity search : {str(e)}")
        raise CustomException(e, sys)

@tool
def lookup_vectordb(query: str)->str:
    """Search within the vectordb to check whether certain options are permitted. Input should be a search query."""
    try: 
        logger.info("Vector tool called")    
        vectordb = load_vectorstore()
        docs = vectordb.similarity_search(query)
        logger.info(f"Vector tool answer returned : {docs}")
        return "\n\n".join([doc.page_content for doc in docs])
    except Exception as e:
        logger.info(f"Exception occure during tool calling lookup vectordb : {str(e)}")
        raise CustomException(e, sys)
    
