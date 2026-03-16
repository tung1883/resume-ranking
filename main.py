import random
import argparse
from resume_parser import parse_resume, parse_job, load_models, parse_resumes
# from resume_ranking import rank_candidates
from resume_generate import resume_generator
import time
from multiprocessing.connection import Client
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import os

skills_list = [
    # Tech
    "Python", "SQL", "Machine Learning", "Deep Learning", "Docker", "Git",

    # Data
    "Data Analysis", "Statistics", "Tableau", "Pandas", "NumPy",

    # Finance
    "Financial Modeling", "Accounting", "Risk Analysis", "Forecasting", "Excel",

    # Marketing
    "SEO", "Content Marketing", "Google Analytics", "Brand Strategy",

    # Soft skills
    "Communication", "Leadership", "Project Management"
]

job_templates = [
    {
        "title": "Data Scientist",
        "skills": ["Python", "Machine Learning", "SQL"]
    },

    {
        "title": "Software Engineer",
        "skills": ["Python", "Docker", "Git"]
    },

    {
        "title": "Financial Analyst",
        "skills": ["Excel", "Financial Modeling", "Accounting"]
    },

    {
        "title": "Marketing Specialist",
        "skills": ["SEO", "Content Marketing", "Google Analytics"]
    }
]

def generate_job_description():
    job = random.choice(job_templates)
    
    return f"""
Title: {job["title"]}
Required skills: {job["skills"]}
"""

if __name__ == "__main__":
    # to receive resume_num from cmd, if cmd does not have, defaulting to 20
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--resume_num", type=int, default=20)
    args = parser.parse_args()
    
    resumes = []
    resume_num = args.resume_num

    print("Generating job and resumes")
    job = generate_job_description()   
    
    if resume_num > 100:
        resume_generator(resume_num)
        
    resumes = [os.path.join("resumes", f"resume_{i + 1}.pdf") for i in range(resume_num)]     
    print("Generating done, now parsing the files")
    start = time.perf_counter()
    load_models()
    parsed_job = parse_job(job)
    
    # --- ProcessPoolExecutor ---
    start1 = time.perf_counter()

    with ProcessPoolExecutor(max_workers=8, initializer=load_models) as executor:
        parsed_resumes = list(executor.map(parse_resume, resumes))

    end1 = time.perf_counter()
    print("ProcessPool time:", end1 - start1, "seconds")

    # --- ThreadPoolExecutor ---
    start1 = time.perf_counter()

    load_models()
    with ThreadPoolExecutor(max_workers=8) as executor:
        parsed_resumes = list(executor.map(parse_resume, resumes))

    end1 = time.perf_counter()
    print("ThreadPool time:", end1 - start1, "seconds")

    # --- Sequential ---
    start1 = time.perf_counter()
    load_models()
    parse_resumes = parse_resumes(resumes)    

    end1 = time.perf_counter()
    print("Sequential time:", end1 - start1, "seconds")
    
    end = time.perf_counter()
    print("Parsing time: ", end - start, "s")

    start = time.perf_counter()
    conn = Client(("localhost", 8000))
    conn.send({"resumes": parsed_resumes, "job": parsed_job})
    ranking = conn.recv()
    end = time.perf_counter()
    
    print(parsed_job)
    print("Candidate Ranking:")
    for name, skills, score in ranking[:10]:
        print(f"{name:<15} | {', '.join(skills):<30} | {score:.2f}")
        # print(f"{name:<15} | {score:.2f}")

    print("Processing time: ", end - start, "s")