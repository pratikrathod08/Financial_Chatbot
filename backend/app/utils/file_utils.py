from sentence_transformers import SentenceTransformer
from PyPDF2 import PdfReader
import pandas as pd
import numpy as np
import docx


def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_csv(file_path: str):
    df = pd.read_csv(file_path)
    return df

def extract_text_from_excel(file_path: str):
    df = pd.read_excel(file_path)
    return df

def extract_text_from_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])




