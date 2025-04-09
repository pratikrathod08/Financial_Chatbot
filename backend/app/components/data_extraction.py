from app.utils.file_utils import read_txt, extract_text_from_pdf, extract_text_from_csv, extract_text_from_excel, extract_text_from_docx

from app.logger import logger

class DataExtractor:

    def __init__(self):
        pass

    logger.info("Data Extraction started")    
    def extract_text(self, file_path: str) -> str:
        logger.info("Text extraction started")
        if file_path.endswith(".pdf"):
            return extract_text_from_pdf(file_path)
        elif file_path.endswith(".docx"):
            return extract_text_from_docx(file_path)
        elif file_path.endswith()(".txt"):
            return read_txt(file_path)
        else:
            logger.info("Unsupported file type")
            raise ValueError("Unsupported file type")
        
    def extract_df(self, file_path: str):
        logger.info("DF Ectraction started")
        if file_path.endswith(".csv"):
            return extract_text_from_csv(file_path)
        elif file_path.endswith(".xlsx"):
            return extract_text_from_excel(file_path)
        else:
            logger.info("Unsupported file type")
            raise ValueError("Unsupported file type")
        
    
