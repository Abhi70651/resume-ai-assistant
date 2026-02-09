import fitz  # PyMuPDF
import re
from pydantic import BaseModel
from typing import Optional

class ResumeData(BaseModel):
    raw_text: str
    page_count: int
    file_name: str

class ResumeParser:
    """Utility class for high-performance PDF text extraction."""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Removes artifacts, extra whitespaces, and non-printable characters."""
        # Remove non-ASCII characters if necessary, but keep punctuation
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def extract_from_bytes(self, pdf_bytes: bytes, file_name: str) -> ResumeData:
        try:
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            full_text = ""
            
            for page in doc:
                full_text += page.get_text("text") + "\n"
            
            cleaned_text = self.clean_text(full_text)
            
            return ResumeData(
                raw_text=cleaned_text,
                page_count=len(doc),
                file_name=file_name
            )
        except Exception as e:
            # In a real industry app, replace with structured logging (e.g., Loguru)
            print(f"Error parsing {file_name}: {str(e)}")
            raise ValueError("Failed to process PDF file.")