from app.utils.file_utils import read_txt, extract_text_from_pdf, extract_text_from_csv, extract_text_from_excel, extract_text_from_docx

class DataExtractor:

    def __init__(self):
        pass

    def extract_text(self, file_path: str) -> str:
        if file_path.endswith(".pdf"):
            return extract_text_from_pdf(file_path)
        elif file_path.endswith(".docx"):
            return extract_text_from_docx(file_path)
        elif file_path.endswith()(".txt"):
            return read_txt(file_path)
        else:
            raise ValueError("Unsupported file type")
        
    def extract_df(self, file_path: str):
        if file_path.endswith(".csv"):
            return extract_text_from_csv(file_path)
        elif file_path.endswith(".xlsx"):
            return extract_text_from_excel(file_path)
        else:
            raise ValueError("Unsupported file type")
        
    
