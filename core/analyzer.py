import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

load_dotenv()

class ResumeAnalyzer:
    def __init__(self):
        # Setup Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def analyze_gap(self, resume_text: str, job_description: str):
        # The System Instruction sets the "Behavioral Guardrails"
        system_instruction = (
            "You are a Senior Technical Recruiter at a Top-Tier Tech Firm. "
            "Your goal is to provide blunt, honest, and actionable feedback. "
            "You must output valid JSON only."
        )
        
        # The User Prompt contains the dynamic data
        user_prompt = f"""
        Analyze this candidate for the following role:
        
        [JOB DESCRIPTION]
        {job_description}
        
        [CANDIDATE RESUME]
        {resume_text}
        
        Return a JSON object with these EXACT keys:
        1. "fit_score_explanation": A concise explanation of why they got their score.
        2. "missing_skills": A list of technical skills found in the JD but not the resume.
        3. "action_plan": A list of 3 specific steps the candidate can take to improve this resume (e.g., 'Add a project using X').
        4. "relevant_experience": Identify the most relevant previous project from their resume for this specific job.
        """
        
        try:
            # We use the 'parts' format for better structure
            response = self.model.generate_content([
                {"role": "user", "parts": [system_instruction + "\n\n" + user_prompt]}
            ])
            
            # Use a more robust JSON extraction
            content = response.text.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            
            return json.loads(content)
        except Exception as e:
            print(f"Gemini Analysis Error: {e}")
            return {
                "fit_score_explanation": "Could not generate analysis.",
                "missing_skills": [],
                "action_plan": ["Review JD manually"],
                "relevant_experience": "N/A"
            }