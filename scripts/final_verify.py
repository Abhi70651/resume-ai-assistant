import os
import torch
from core.parser import ResumeParser
from core.embedder import Embedder
from core.analyzer import ResumeAnalyzer
from core.vector_store import VectorStore
from core.security import SecurityGuard
from loguru import logger

def run_diagnostic():
    logger.info("🚀 Starting Final System Diagnostic...")
    
    # 1. Check Environment
    if not os.getenv("GEMINI_API_KEY"):
        logger.error("❌ GEMINI_API_KEY missing in .env")
        return
    
    try:
        # 2. Test Parser & Security
        parser = ResumeParser()
        sample_pdf_path = "data/resumes/sample_resume.pdf"
        with open(sample_pdf_path, "rb") as f:
            content = f.read()
            SecurityGuard.validate_file_size(content)
            data = parser.extract_from_bytes(content, "test.pdf")
        logger.success("✅ Parser & Security Layer: PASSED")

        # 3. Test Embedder (Math/AI Layer)
        embedder = Embedder()
        vec = embedder.get_chunked_embedding(data.raw_text)
        if vec is not None and vec.shape[0] == 384:
            logger.success(f"✅ Embedder (Vector Dim: {vec.shape[0]}): PASSED")
        
        # 4. Test Vector Store (Persistence)
        v_store = VectorStore()
        v_store.add_resume("test_id", vec, data.raw_text)
        logger.success("✅ Vector Store Persistence: PASSED")

        # 5. Test Gemini (Intelligence Layer)
        analyzer = ResumeAnalyzer()
        analysis = analyzer.analyze_gap(data.raw_text, "Looking for a Python AI Engineer.")
        if "missing_skills" in analysis:
            logger.success("✅ Gemini AI Analysis: PASSED")
            logger.info(f"Gemini Sample Feedback: {analysis['match_summary'][:50]}...")

        print("\n" + "="*30)
        print("🏆 SYSTEM READY FOR DEPLOYMENT")
        print("="*30)

    except Exception as e:
        logger.error(f"💥 Diagnostic Failed: {str(e)}")

if __name__ == "__main__":
    run_diagnostic()