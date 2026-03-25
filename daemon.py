from multiprocessing.connection import Listener
from resume_ranking import rank_candidates
from resume_parser import parse_job, load_models

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

            resumes = data["resumes"]  
            job_text = data["job_text"]

            job = parse_job(job_text)
            if not job["skills"]:
                # No skills extracted — return applicants unranked with score 0
                conn.send([
                    {"name": r["name"], "skills": [], "score": 0.0}
                    for r in resumes
                ])
                conn.close()
                continue
            
            ranking = rank_candidates(resumes, job)
            print(ranking) 
            
            conn.send([
                {"name": r[0], "skills": r[1], "score": float(r[2])}
                for r in ranking
            ])
            
            conn.close()
        finally:
            conn.close()
