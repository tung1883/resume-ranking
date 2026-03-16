from multiprocessing import Pool
from worker import init_model, rank_candidates_batch

pool = None

def start_workers(model_path):
    global pool

    pool = Pool(
        processes=4,
        initializer=init_model,
        initargs=(model_path,)
    )

def process_jobs(batches):
    return pool.map(rank_candidates_batch, batches)

if __name__ == "__main__":
    start_workers("./models/all-MiniLM-L6-v2")
    print("Workers ready")

    # simulate waiting for requests
    import time
    time.sleep(5)

    tasks = [
        (["resume1"], "jobA"),
        (["resume2"], "jobB"),
        (["resume3"], "jobC"),
        (["resume4"], "jobD"),
    ]

    batches = [tasks[i:i + 2] for i in range(0, len(tasks), 2)]

    results = process_jobs(batches)

    print(results)

    pool.close()
    pool.join()
