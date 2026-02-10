from core.embedder import Embedder

def run_experiment():
    embedder = Embedder()
    
    # 1. The Job Description
    job_desc = "Senior Backend Developer: 5+ years experience in Python, FastAPI, and PostgreSQL. Must understand Microservices and Docker."

    # 2. Different Resume Personas
    personas = {
        "Perfect Match": "Senior Backend Engineer with 6 years of Python experience. Expert in FastAPI, PostgreSQL, and deploying microservices via Docker.",
        "Keyword Stuffer (No Context)": "Python Python Python FastAPI FastAPI Docker Docker PostgreSQL PostgreSQL PostgreSQL.",
        "Junior/Entry Level": "Fresh graduate with a focus on Python and basic web development. Familiar with SQL and learning FastAPI.",
        "Adjacent Role (Data Science)": "Data Scientist with 5 years of Python experience. Specialized in Machine Learning, Pandas, and SQL databases. Used Docker for model serving.",
        "Irrelevant": "Graphic Designer with 10 years experience in Adobe Creative Suite, UI/UX design, and brand identity."
    }

    print(f"Target Job: {job_desc[:60]}...\n")
    job_vec = embedder.get_embedding(job_desc)

    for name, text in personas.items():
        res_vec = embedder.get_embedding(text)
        score = embedder.compute_similarity(job_vec, res_vec)
        print(f"[{name}] -> Score: {score:.4f}")

if __name__ == "__main__":
    run_experiment()