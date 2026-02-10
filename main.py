import os
from core.parser import ResumeParser
from core.embedder import Embedder
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

def run_day_1_test():
    parser = ResumeParser()
    embedder = Embedder()

    # 1. Parse your resume (from Day 0)
    with open("data/resumes/sample_resume.pdf", "rb") as f:
        resume_data = parser.extract_from_bytes(f.read(), "sample_resume.pdf")

    # 2. Define a Mock Job Description
    job_description = """
    We are looking for an AI Engineer with experience in Python and LLMs. 
    The ideal candidate should know FastAPI and have worked with embeddings.
    Knowledge of Information Security is a plus.
    """

    # 3. Vectorize both
    print("🧠 Vectorizing data...")
    resume_vec = embedder.get_embedding(resume_data.raw_text)
    job_vec = embedder.get_embedding(job_description)

    # 4. Compare
    match_score = embedder.compute_similarity(resume_vec, job_vec)
    
    print(f"\n--- Day 1 Result ---")
    print(f"Match Score: {match_score:.4f} ({match_score*100:.1f}%)")
    print("--------------------")

if __name__ == "__main__":
    run_day_1_test()