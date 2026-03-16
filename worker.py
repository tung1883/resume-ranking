from sentence_transformers import SentenceTransformer
import os

MODEL = None


def init_model(model_path):
    global MODEL

    print(f"Worker {os.getpid()} loading model...")
    MODEL = SentenceTransformer(model_path)

    print(f"Worker {os.getpid()} ready")


def rank_candidates_batch(batch):
    results = []

    for resumes, job in batch:
        emb = MODEL.encode(resumes)
        results.append((job, len(emb)))

    return results
