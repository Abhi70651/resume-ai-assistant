from fpdf import FPDF

class MockResume(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Abhay Pandey - AI Engineer Candidate", ln=True, align="C")
        self.ln(5)

    def section_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 10, title, ln=True, fill=True)
        self.ln(2)

    def body_text(self, text):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 8, text)
        self.ln(4)

def create_resume():
    pdf = MockResume()
    pdf.add_page()

    pdf.section_title("Summary")
    pdf.body_text("Experienced AI Engineer with a focus on Information Security and LLM integration. Proficient in Python, FastAPI, and Vector Databases.")

    pdf.section_title("Skills")
    pdf.body_text("- Languages: Python, C++, Bash\n- AI: SentenceTransformers, Gemini API, PyTorch\n- Security: eBPF monitoring, Cryptography")

    pdf.section_title("Experience")
    pdf.body_text("Senior AI Researcher | TechCorp (2024-Present)\n- Led the development of a real-time intrusion detection system using eBPF.\n- Optimized embedding pipelines for large-scale document retrieval.")

    # Create the data directory if it doesn't exist
    import os
    os.makedirs("data/resumes", exist_ok=True)
    
    pdf.output("data/resumes/sample_resume.pdf")
    print("✅ Created: data/resumes/sample_resume.pdf")

if __name__ == "__main__":
    create_resume()