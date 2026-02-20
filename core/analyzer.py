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
        prompt = f"""
        You are an expert Technical Recruiter. Analyze the following Resume against the Job Description.
        
        Resume: {resume_text}
        Job Description: {job_description}
        
        Provide a response strictly in JSON format with these keys:
        - match_summary: (A 2-sentence overview of the fit)
        - missing_skills: (List of 3-5 technical skills present in JD but missing in Resume)
        - profile_strengths: (List of top 3 strengths)
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Standardizing the response - Gemini sometimes wraps JSON in markdown ```json
            clean_json = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except Exception as e:
            return {
                "match_summary": "Error analyzing feedback.",
                "missing_skills": [],
                "profile_strengths": []
            }