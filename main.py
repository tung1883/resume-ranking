import random
from resume_parser import parse_resume
from resume_ranking import rank_candidates
    
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

    return {
        "title": job["title"],
        "required_skills": job["skills"]
    }
    
if __name__ == "__main__":

    job = generate_job_description()

    print("Job Title:", job["title"])
    print("Required Skills:", job["required_skills"])
    print()

    resumes = []

    for i in range(10):

        path = f".\\resume_{i+1}.pdf"

        parsed = parse_resume(path, skills_list)
        resumes.append(parsed)

    ranking = rank_candidates(resumes, job)

    print("Candidate Ranking:")
    for name, skills, score in ranking:
        print(name, "| skills:", skills, "| score:", round(score, 2))
