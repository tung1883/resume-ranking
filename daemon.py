from multiprocessing.connection import Listener
from resume_ranking import rank_candidates
import time

if __name__ == "__main__":
    listener = Listener(("localhost", 8000))
    print("Daemon worker running...")

    while True:
        conn = listener.accept()

        try:
            data = conn.recv()
            
            if data == "STOP":
                conn.send("STOPPING DAEMON...")
                conn.close()
                break

            resumes = data["resumes"]
            job = data["job"]

            if not resumes or not job: 
                conn.send("WRONG DATA")
                conn.close()
        
            rank_start = time.perf_counter()
            ranking = rank_candidates(resumes, job)
            conn.send(ranking)    
        finally:
            conn.close()
