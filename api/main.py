from fastapi import FastAPI, UploadFile, File, Form
from core.parser import ResumeParser
from core.embedder import Embedder
import uvicorn

app = FastAPI(title="AI Resume Matcher API")

# Initialize our "Services" once at startup
parser = ResumeParser()
embedder = Embedder()

@app.post("/match")
async def match_resume(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...)
):
    # 1. Read the uploaded PDF
    file_bytes = await resume_file.read()
    
    # 2. Parse
    resume_data = parser.extract_from_bytes(file_bytes, resume_file.filename)
    
    # 3. Embed & Compare (Using our new Chunking logic!)
    resume_vec = embedder.get_chunked_embedding(resume_data.raw_text)
    job_vec = embedder.get_embedding(job_description)
    
    score = embedder.compute_similarity(resume_vec, job_vec)
    
    return {
        "filename": resume_file.filename,
        "match_score": round(score * 100, 2),
        "pages": resume_data.page_count,
        "status": "success"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)