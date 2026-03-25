import time
from sentence_transformers import SentenceTransformer
import numpy as np
import os

model_path = "./models/all-MiniLM-L6-v2"

if os.path.exists(model_path):
    model = SentenceTransformer(model_path)
else:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    model.save(model_path)

level_sentences = {
    1: "basic familiarity with the skill",
    2: "used the skill in work or projects",
    3: "applied the skill to build or deliver results",
    4: "led work or had expert responsibility using the skill"
}
level_embeddings = {
    level: model.encode(sentence)
    for level, sentence in level_sentences.items()
}
level_keys = list(level_embeddings.keys())
level_keys_arr = np.array(level_keys)
level_matrix = np.array(list(level_embeddings.values()))
    
TOTAL_SKILL_LEVELS = 4

def infer_skill_levels(skills):
    contexts = [item["context"] for item in skills]
    skill_names = [item["skill"] for item in skills]

    context_vecs = model.encode(contexts, batch_size=256)

    level_keys = list(level_embeddings.keys())
    level_matrix = np.array(list(level_embeddings.values()))

    # sims = cosine_similarity(context_vecs, level_matrix)
    sims = context_vecs @ level_matrix.T

    levels = {}

    for skill, row in zip(skill_names, sims):
        best_idx = np.argmax(row)
        levels[skill] = level_keys[best_idx]

    return levels

def compute_skill_score(candidate, job_skill_vecs):
    skill_levels = infer_skill_levels(candidate["skills"])
    skills = list(skill_levels.keys())
    levels = np.array(list(skill_levels.values()))
    c_skill_vecs = model.encode(skills)
    # sims = cosine_similarity(c_skill_vecs, job_skill_vecs)
    sims = c_skill_vecs @ job_skill_vecs.T
    weighted = sims * (levels[:, None] / TOTAL_SKILL_LEVELS)
    return weighted.sum()

# change job["education"] to auto-find the edu. from text
def compute_education_score(candidate, job):
    if not job["edu"] or len(job["edu"] == 0):
        return None

    if not candidate.get("education"):
        return 0

    candidate_text = " ".join(candidate["education"])
    job_text = job["education"]

    cand_vec = model.encode(candidate_text)
    job_vec = model.encode(job_text)

    # similarity = cosine_similarity([cand_vec], [job_vec])[0][0]
    similarity = cand_vec @ job_vec
    
    return similarity

def compute_candidate_score(candidate, job_skill_vecs):
    skill_score = compute_skill_score(candidate, job_skill_vecs)
    return skill_score

    # education_score = compute_education_score(candidate, job)
    # if education_score is None: education_score = 0

    # return 0.7 * skill_score + 0.3 * education_score

def rank_candidates(resumes, job):
    t0 = time.perf_counter()

    job_skill_vecs = model.encode(job["skills"], normalize_embeddings=True)
    t1 = time.perf_counter()
    print("Encode job skills:", t1 - t0)

    all_contexts = []
    all_skills = []
    resume_indices = []
    resume_names = []

    for i, r in enumerate(resumes):
        resume_names.append(r["name"])
        for item in r["skills"]:
            all_contexts.append(item["context"])
            all_skills.append(item["skill"])
            resume_indices.append(i)

    t2 = time.perf_counter()
    print("Collect data:", t2 - t1)

    context_vecs = model.encode(
        all_contexts,
        batch_size=256,
        normalize_embeddings=True
    )

    t3 = time.perf_counter()
    print("Encode contexts:", t3 - t2)

    sims = context_vecs @ level_matrix.T
    best_levels = np.argmax(sims, axis=1)

    levels = level_keys_arr[best_levels]

    t4 = time.perf_counter()
    print("Infer levels:", t4 - t3)

    all_skill_vecs = model.encode(
        all_skills,
        batch_size=256,
        normalize_embeddings=True
    )

    t5 = time.perf_counter()
    print("Encode skills:", t5 - t4)

    sims = all_skill_vecs @ job_skill_vecs.T

    weighted_scores = sims * (levels[:, None] / TOTAL_SKILL_LEVELS)
    skill_scores = weighted_scores.sum(axis=1)

    t6 = time.perf_counter()
    print("Compute similarity:", t6 - t5)

    resume_scores = np.zeros(len(resumes))
    np.add.at(resume_scores, resume_indices, skill_scores)

    t7 = time.perf_counter()
    print("Aggregate scores:", t7 - t6)

    ranked = []
    for i, r in enumerate(resumes):
        skills = [s["skill"] for s in r["skills"]]
        ranked.append((resume_names[i], skills, resume_scores[i]))

    ranked.sort(key=lambda x: x[2], reverse=True)

    t8 = time.perf_counter()
    print("Sorting:", t8 - t7)

    print("Total:", t8 - t0)

    return ranked
