from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import cosine_similarity
model = SentenceTransformer("all-MiniLM-L6-v2")

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


def infer_skill_levels(skills):

    levels = {}

    for item in skills:

        skill = item["skill"]
        context = item["context"]

        context_vec = model.encode(context)

        best_level = 1
        best_score = -1

        for level, ref_vec in level_embeddings.items():

            sim = cosine_similarity([context_vec], [ref_vec])[0][0]

            if sim > best_score:
                best_score = sim
                best_level = level

        levels[skill] = best_level

    return levels


def compute_skill_score(candidate, job):

    required_skills = job["required_skills"]

    skill_levels = infer_skill_levels(candidate["skills"])

    score = 0

    for skill in required_skills:

        if skill in skill_levels:

            score += skill_levels[skill] / 4

    return score / len(required_skills)


def compute_education_score(candidate, job):

    if "education" not in job or not job["education"]:
        return None

    if not candidate.get("education"):
        return 0

    candidate_text = " ".join(candidate["education"])
    job_text = job["education"]

    cand_vec = model.encode(candidate_text)
    job_vec = model.encode(job_text)

    similarity = cosine_similarity([cand_vec], [job_vec])[0][0]

    return similarity


def compute_candidate_score(candidate, job):

    skill_score = compute_skill_score(candidate, job)

    education_score = compute_education_score(candidate, job)

    if education_score is None:
        return skill_score

    return 0.7 * skill_score + 0.3 * education_score


def rank_candidates(resumes, job):

    ranked = []

    for r in resumes:

        score = compute_candidate_score(r, job)

        skill_names = [s["skill"] for s in r["skills"]]
        ranked.append((r["name"], skill_names, score))

    ranked.sort(key=lambda x: x[2], reverse=True)

    return ranked
