import streamlit as st
import requests
import os

st.set_page_config(page_title="AI Resume Matcher", page_icon="📄", layout="wide")

st.title("AI Resume Screening & Job Match Assistant")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    </style>
    """, unsafe_allow_html=True)
# 1. Sidebar for Inputs
with st.sidebar:
    st.header("Upload Details")
    job_desc = st.text_area("Paste Job Description here:", height=300)
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    analyze_btn = st.button("Analyze Match", type="primary")

# 2. Main Content Area
if analyze_btn:
    if not job_desc or not uploaded_file:
        st.error("Please provide both a job description and a resume.")
    else:
        with st.spinner("🧠 AI is analyzing your match..."):
            try:
                # Prepare data for FastAPI
                files = {"resume_file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                data = {"job_description": job_desc}
                
                # Call our FastAPI backend
                BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
                
                response = requests.post(f"{BACKEND_URL}/match", data=data, files=files)
                result = response.json()

                if response.status_code == 200:
                    # 3. Display Results
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.metric(label="Match Score", value=f"{result['match_score']}%")
                        # Simple visual progress bar
                        st.progress(result['match_score'] / 100)
                    
                    with col2:
                        analysis = result.get('analysis', {})
                        st.subheader("Match Summary")
                        st.write(analysis.get("match_summary", "No summary available."))

                    st.markdown("---")
                    
                    # 4. Detailed Breakdown
                    c1, c2 = st.columns(2)
                    with c1:
                        st.info(" **Action Plan to Match**")
                        for step in analysis.get("action_plan", []):
                            st.write(f"- {step}")
                            
                    with c2:
                        st.warning("**Missing Skills**")
                        for gap in analysis.get("missing_skills", []):
                            st.write(f"- {gap}")
                    st.success(f"**Most Relevant Experience:** {analysis.get('relevant_experience')}")
                else:
                    st.error("API Error: Could not process the request.")

            except Exception as e:
                st.error(f"Connection Error: Is the FastAPI server running? \n({e})")
st.header("Batch Candidate Ranking")
multi_files = st.file_uploader("Upload Multiple Resumes", type=["pdf"], accept_multiple_files=True)

if st.button("Rank Candidates") and multi_files:
    with st.spinner("Ranking candidates..."):
        # Prepare files for the multipart request
        files = [("resume_files", (f.name, f.getvalue(), "application/pdf")) for f in multi_files]
        data = {"job_description": job_desc}
        
        response = requests.post("http://127.0.0.1:8000/rank", data=data, files=files)
        
        if response.status_code == 200:
            rankings = response.json()["rankings"]
            # Display as a nice table
            st.table(rankings)
        else:
            st.error("Failed to rank resumes.")
            
if analyze_btn:
    if not job_desc or not uploaded_file:
        st.error("Please provide both details.")
    else:
        with st.spinner("AI is analyzing..."):
            response = None # Initialize to avoid NameError
            try:
                files = {"resume_file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                data = {"job_description": job_desc}
                
                response = requests.post(f"{BACKEND_URL}/match", data=data, files=files)
                
                # Only check status_code if response actually exists
                if response is not None and response.status_code == 200:
                    result = response.json()
                    # ... rest of your display logic ...
                else:
                    st.error(f"Backend returned an error: {response.status_code if response else 'No Response'}")

            except Exception as e:
                st.error(f"Connection Error: {e}")