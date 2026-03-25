from multiprocessing.connection import Listener
import os
import signal
import sys
from resume_ranking import rank_candidates
from resume_parser import parse_job, parse_resumes, load_models

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_UPLOADS = os.path.join(PROJECT_ROOT, "backend", "uploads")

running = True

def handle_signal(sig, frame):
    global running
    print("\nShutting down...")
    running = False
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    listener = Listener(("localhost", 8000))
    # unblock every 1s to check signals
    listener._listener._socket.settimeout(1.0)
    print("Daemon worker running...")
    load_models()

    while running:
        try:
            conn = listener.accept()
        except OSError:
            continue  # timeout, loop back and check `running`

        try:
            data = conn.recv()
            if data == "STOP":
                conn.send("STOPPING")
                conn.close()
                break

            pdf_paths = []
            for r in data.get("resumes", []):
                rel_path = r.get("path")
                if rel_path:
                    rel_path = rel_path.lstrip("./")
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
            conn.send([
                {"name": r[0], "skills": r[1],
                    "score": float(r[2]), "email": r[3]}
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

    listener.close()
