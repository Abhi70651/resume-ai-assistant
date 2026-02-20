from core.parser import ResumeParser
from core.embedder import Embedder
from scripts.generate_test_resume import MockResume # Reusing your generator
import os

def create_long_resume():
    pdf = MockResume()
    pdf.add_page()
    pdf.section_title("Summary")
    pdf.body_text("AI Engineer and Security Specialist.")
    
    # Fill 3 pages with fluff to push important info to the bottom
    for i in range(150):
        pdf.section_title(f"Project Number {i}")
        pdf.body_text("This is a filler project description to increase the word count of the document significantly.")
    
    # The "Gold" is at the very bottom
    pdf.add_page()
    pdf.section_title("Crucial Skills")
    pdf.body_text("Expertise in FastAPI, Gemini API, and SentenceTransformers. Information Security Master.")
    
    pdf.output("data/resumes/long_resume.pdf")

def run_stress_test():
    create_long_resume()
    parser = ResumeParser()
    embedder = Embedder()
    
    with open("data/resumes/long_resume.pdf", "rb") as f:
        data = parser.extract_from_bytes(f.read(), "long_resume.pdf")

    job_desc = "Seeking an expert in FastAPI, Gemini API, and SentenceTransformers."

    # Standard approach (limited view)
    std_vec = embedder.get_embedding(data.raw_text)
    job_vec = embedder.get_embedding(job_desc)
    std_score = embedder.compute_similarity(std_vec, job_vec)

    # Chunked approach (full view)
    chunk_vec = embedder.get_chunked_embedding(data.raw_text)
    chunk_score = embedder.compute_similarity(chunk_vec, job_vec)

    print(f"\n--- Stress Test Results ---")
    print(f"Standard Score: {std_score:.4f}")
    print(f"Chunked Score:  {chunk_score:.4f}")
    print(f"Improvement:    {(chunk_score - std_score)*100:.2f}%")
    print("---------------------------\n")

if __name__ == "__main__":
    run_stress_test()