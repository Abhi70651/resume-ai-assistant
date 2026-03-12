from fastapi import FastAPI, UploadFile, File, Form
from core.security import SecurityGuard, logger
from core.parser import ResumeParser
from core.embedder import Embedder
import uvicorn
from core.analyzer import ResumeAnalyzer
from core.vector_store import VectorStore
from typing import List

app = FastAPI(title="AI Resume Matcher API")

# Initialize our "Services" once at startup
parser = ResumeParser()
embedder = Embedder()
analyzer = ResumeAnalyzer()
v_store=VectorStore()

@app.post("/match")
async def match_resume(
    job_description: str = Form(...),
    resume_file: UploadFile = File(...)
):
    logger.info(f"Processing request for file: {resume_file.filename}")
    
    try:
        content = await resume_file.read()
        
        # 1. Security Check: File Size
        SecurityGuard.validate_file_size(content)
        
        # 2. Extract & Sanitize
        resume_data = parser.extract_from_bytes(content, resume_file.filename)
        safe_resume_text = SecurityGuard.sanitize_input(resume_data.raw_text)
        # 1. Read the uploaded PDF
        file_bytes = await resume_file.read()
        
        # 2. Parse
        resume_data = parser.extract_from_bytes(file_bytes, resume_file.filename)
        #2.5 get gemini analysis
        analysis = analyzer.analyze_gap(resume_data.raw_text, job_description)
        # 3. Embed & Compare (Using our new Chunking logic!)
        resume_vec = embedder.get_chunked_embedding(resume_data.raw_text)
        job_vec = embedder.get_embedding(job_description)
        
        score = embedder.compute_similarity(resume_vec, job_vec)
        v_store.add_resume(
            resume_id=resume_file.filename, 
            embedding=resume_vec, 
            text=resume_data.raw_text
        )
    except Exception as e:
        logger.error(f"Failed to process {resume_file.filename}: {str(e)}")
        return {"error": "Internal processing error", "status": "failed"}
    return {
        "filename": resume_file.filename,
        "match_score": round(score * 100, 2),
        "analysis":analysis,
        "status": "success"
    }

@app.post("/rank")
async def rank_resumes(
    job_description: str = Form(...),
    resume_files: List[UploadFile] = File(...)
):
    results = []
    job_vec = embedder.get_embedding(job_description)

    for file in resume_files:
        content = await file.read()
        # 1. Extract
        resume_data = parser.extract_from_bytes(content, file.filename)
        # 2. Embed (using chunking for accuracy)
        resume_vec = embedder.get_chunked_embedding(resume_data.raw_text)
        # 3. Score
        score = embedder.compute_similarity(resume_vec, job_vec)
        
        results.append({
            "filename": file.filename,
            "score": round(score * 100, 2)
        })
    
    # 4. Sort by score (Highest first)
    ranked_results = sorted(results, key=lambda x: x['score'], reverse=True)
    
    return {"rankings": ranked_results}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.post("/match")
async def match_resume(job_description: str = Form(...), resume_file: UploadFile = File(...)):
    logger.info(f"Processing request for file: {resume_file.filename}")
    
    try:
        content = await resume_file.read()
        
        # 1. Security Check: File Size
        SecurityGuard.validate_file_size(content)
        
        # 2. Extract & Sanitize
        resume_data = parser.extract_from_bytes(content, resume_file.filename)
        safe_resume_text = SecurityGuard.sanitize_input(resume_data.raw_text)
        
        # ... rest of the embedding and analysis logic ...
        
    except Exception as e:
        logger.error(f"Failed to process {resume_file.filename}: {str(e)}")
        return {"error": "Internal processing error", "status": "failed"}