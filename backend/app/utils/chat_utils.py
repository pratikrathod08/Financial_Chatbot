import os, sys 
import pandas as pd 
import PyPDF2
import docx


def read_pdf(path):
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

def read_docx(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def read_csv(path):
    df = pd.read_csv(path)
    return df.to_string()

def read_excel(path):
    df = pd.read_excel(path)
    return df.to_string()

def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()