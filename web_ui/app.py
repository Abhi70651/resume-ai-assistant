import streamlit as st
import requests

st.set_page_config(page_title="AI Resume Matcher", page_icon="📄", layout="wide")

st.title("🚀 AI Resume Screening & Job Match Assistant")
st.markdown("---")

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
                response = requests.post("http://127.0.0.1:8000/match", data=data, files=files)
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
                        st.success("✅ **Profile Strengths**")
                        for strength in analysis.get("profile_strengths", []):
                            st.write(f"- {strength}")
                            
                    with c2:
                        st.warning("⚠️ **Missing Skills / Gaps**")
                        for gap in analysis.get("missing_skills", []):
                            st.write(f"- {gap}")

                else:
                    st.error("API Error: Could not process the request.")

            except Exception as e:
                st.error(f"Connection Error: Is the FastAPI server running? \n({e})")