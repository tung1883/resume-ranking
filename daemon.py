from multiprocessing.connection import Listener
import os

from resume_ranking import rank_candidates
from resume_parser import parse_job, parse_resumes, load_models

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_UPLOADS = os.path.join(PROJECT_ROOT, "backend", "uploads")

if __name__ == "__main__":
    listener = Listener(("localhost", 8000))
    print("Daemon worker running...")
    load_models()
    while True:
        conn = listener.accept()
        try:
            data = conn.recv()

            if data == "STOP":
                conn.send("STOPPING")
                conn.close()
                break

            # pdf_paths = [r["path"] for r in data["resumes"] if r.get("path")]
            pdf_paths = []
            for r in data.get("resumes", []):
                rel_path = r.get("path")
                if rel_path:
                    # Remove leading ./ if present
                    rel_path = rel_path.lstrip("./")
                    # Join with backend/uploads folder
                    full_path = os.path.join(PROJECT_ROOT, "backend", rel_path)
                    pdf_paths.append(full_path)
            job_text = data["job_text"]

            parsed_resumes = parse_resumes(pdf_paths)
            for parsed, original in zip(parsed_resumes, data["resumes"]):
                parsed["account_email"] = original["email"]
                
            job = parse_job(job_text)

            if not job["skills"]:
                conn.send([
                    {"name": r["name"], "skills": [], "score": 0.0}
                    for r in parsed_resumes
                ])
                conn.close()
                continue

            ranking = rank_candidates(parsed_resumes, job)

            # conn.send([
            #     {"name": r[0], "skills": r[1], "score": float(r[2])}
            #     for r in ranking
            # ])

            conn.send([
                {"name": r[0], "skills": r[1], "score": float(r[2]), "email": r[3]}
                for r in ranking
            ])
    
        except Exception as e:
            print(f"Error processing request: {e}")
            try:
                conn.send({"error": str(e)})
            except:
                pass
        finally:
            conn.close()
