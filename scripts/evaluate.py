import json
from core.embedder import Embedder
from core.parser import ResumeParser
import os

class Evaluator:
    def __init__(self):
        self.embedder = Embedder()
        self.parser = ResumeParser()

    def calculate_precision_at_1(self, expected, actual):
        """Checks if the top-ranked resume is the one we expected."""
        return 1 if expected[0] == actual[0] else 0

    def run_benchmark(self, benchmark_path="data/benchmark.json"):
        with open(benchmark_path, "r") as f:
            tests = json.load(f)

        for test in tests:
            jd = test["job_description"]
            expected = test["expected_ranking"]
            
            # Simulate the ranking
            scores = []
            for filename in expected:
                # Assuming files exist in data/resumes/
                path = f"data/resumes/{filename}"
                with open(path, "rb") as f:
                    data = self.parser.extract_from_bytes(f.read(), filename)
                    vec = self.embedder.get_chunked_embedding(data.raw_text)
                    job_vec = self.embedder.get_embedding(jd)
                    score = self.embedder.compute_similarity(vec, job_vec)
                    scores.append({"name": filename, "score": score})

            # Sort by score
            actual_ranking = [item["name"] for item in sorted(scores, key=lambda x: x["score"], reverse=True)]
            
            p1 = self.calculate_precision_at_1(expected, actual_ranking)
            print(f"--- Benchmark Result ---")
            print(f"Expected: {expected}")
            print(f"Actual:   {actual_ranking}")
            print(f"Precision@1: {p1 * 100}%")

if __name__ == "__main__":
    Evaluator().run_benchmark()