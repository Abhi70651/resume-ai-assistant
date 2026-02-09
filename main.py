import os
from core.parser import ResumeParser

def test_extraction():
    # 1. Initialize our parser
    parser = ResumeParser()
    
    # 2. Path to a sample resume (Ensure you put a PDF here!)
    sample_path = "data/resumes/sample_resume.pdf"
    
    if not os.path.exists(sample_path):
        print(f"❌ Error: Please place a PDF at {sample_path}")
        return

    # 3. Read the file as bytes (simulating a file upload)
    with open(sample_path, "rb") as f:
        file_bytes = f.read()
    
    # 4. Extract and Validate
    try:
        resume_data = parser.extract_from_bytes(file_bytes, "sample_resume.pdf")
        
        print("--- Extraction Successful ---")
        print(f"File: {resume_data.file_name}")
        print(f"Pages: {resume_data.page_count}")
        print(f"Text Preview (First 200 chars): {resume_data.raw_text[:200]}...")
        print("-----------------------------")
        
    except Exception as e:
        print(f"❌ Extraction failed: {e}")

if __name__ == "__main__":
    test_extraction()