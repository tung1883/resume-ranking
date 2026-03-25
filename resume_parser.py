import re
import pdfplumber
import spacy
from spacy.matcher import Matcher
from skill_ner_model.data_parser import clean_text

base_model = None
ner_model = None

def load_models():
    global base_model, ner_model

    if base_model is None:
        base_model = spacy.load("en_core_web_sm")

    if ner_model is None:
        ner_model = spacy.load(".\\skill_ner_model\\output\\model-best", disable=["tagger", "parser", "lemmatizer"])

def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text(y_tolerance=.5) + "\n"

    return text

def extract_contact_number(text):
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    return match.group() if match else None

def extract_email(text):
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    return match.group() if match else None

GENERIC_SKILLS = {
    "problem solving",
    "problem solve",
    "industry project",
    "industry projects",
    "professional project",
    "professional projects",
    "core skills",
    "teamwork",
    "communication",
    "leadership",
    "efficiency",
    "collaboration",
    "cross functional team",
    "project management",
    "efficiency",
    "engineer insight",
    "monitoring"
}

def extract_skills(text, name=None, email=None):
    if (name != None):
        text = text.replace(name, "")
    else:
        print("extract_skills: Name of applicant is not provided, skip removing name")

    if (email != None):
        text = text.replace(email, "")
    else:
        print("extract_skills: Email of applicant is not provided, skip removing email")

    text = re.sub(
        r".*\b(bachelor|master|phd|bsc|msc|mba)\b.*\n?",
        "",
        text,
        flags=re.IGNORECASE
    )  # remove educational degree

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    merged_lines = []
    
    for l in lines:
        # check for sentences that are on 2 different lines
        if merged_lines and not re.match(r"^[-*•]|^[A-Z]", l):
            merged_lines[-1] += " " + clean_text(
                l, remove_parentheses=True, split_hyphens=True, remove_special_char=True)
        else:
            merged_lines.append(clean_text(
                l, remove_parentheses=True, split_hyphens=True, remove_special_char=True))
    
    skills = []
    for doc in ner_model.pipe(merged_lines, batch_size=128):
        for ent in doc.ents:
            if ent.label_ != "SKILL" or ent.text in GENERIC_SKILLS or len(ent.text.split()) >= 5:
                continue
                
            skills.append({
                "skill": ent.text,
                "context": doc.text
            })
                
    return skills

def extract_education(text):
    pattern = r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.\w+|\bBachelor(?:'s)?|\bMaster(?:'s)?|\bPh\.D)\s(?:\w+\s)*\w+"
    return re.findall(pattern, text)

# def extract_name(resume_text):
#     matcher = Matcher(base_model.vocab)

#     patterns = [
#         [{'POS': 'PROPN'}, {'POS': 'PROPN'}],
#         [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],
#         [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]
#     ]

#     matcher.add("NAME", patterns)

#     doc = base_model(resume_text)
#     matches = matcher(doc)

#     for match_id, start, end in matches:
#         span = doc[start:end]
#         return span.text

#     return None

def extract_name(text):
    lines = text.split("\n")[:5]

    name_pattern = re.compile(r"^[A-Z][a-z]+(?:\s[A-Z][a-z]+){1,3}$")

    for line in lines:
        line = line.strip()

        if name_pattern.match(line):
            return line

    return None

def parse_resume(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    name = extract_name(text)
    email = extract_email(text)

    result = {
        "name": name,
        "email": email,
        "phone": extract_contact_number(text),
        "skills": extract_skills(text, name=name, email=email),
        "education": extract_education(text),
        "raw_text": text
    }

    return result

def parse_job(job_desc):
    email = extract_email(job_desc)
    phone = extract_contact_number(job_desc)
    edu = extract_education(job_desc)
    
    if email: job_desc = job_desc.replace(email, "")
    if phone: job_desc = job_desc.replace(phone, "")
    if edu: job_desc = job_desc.replace(edu, "")
    skills = extract_skills(job_desc)
    
    return {
        "text": job_desc,
        "skills": [s["skill"] for s in skills],
        "email": email,
        "phone": phone,
        "edu": edu
    }
    
### batched parsing
def preprocess_resume(text, name=None, email=None):
    if name:
        text = text.replace(name, "")

    if email:
        text = text.replace(email, "")

    text = re.sub(
        r".*\b(bachelor|master|phd|bsc|msc|mba)\b.*\n?",
        "",
        text,
        flags=re.IGNORECASE
    )

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    merged_lines = []

    for l in lines:
        cleaned = clean_text(
            l,
            remove_parentheses=True,
            split_hyphens=True,
            remove_special_char=True
        )

        if merged_lines and not re.match(r"^[-*•]|^[A-Z]", l):
            merged_lines[-1] += " " + cleaned
        else:
            merged_lines.append(cleaned)

    return merged_lines

def extract_skills_batch(resumes):
    """
    resumes = [
        {"text": text1, "name": name1, "email": email1},
        {"text": text2, "name": name2, "email": email2},
    ]
    """

    all_lines = []
    resume_index = []

    for i, r in enumerate(resumes):
        lines = preprocess_resume(r["text"], r.get("name"), r.get("email"))

        for line in lines:
            all_lines.append(line)
            resume_index.append(i)

    # run NER once for all lines
    docs = ner_model.pipe(all_lines, batch_size=512)

    results = [[] for _ in resumes]

    for doc, idx in zip(docs, resume_index):
        for ent in doc.ents:
            skill = ent.text.lower().strip()

            if ent.label_ != "SKILL":
                continue
            if skill in GENERIC_SKILLS:
                continue
            if len(skill.split()) >= 5:
                continue

            results[idx].append({
                "skill": skill,
                "context": doc.text
            })

    return results

def parse_resumes(pdf_paths):
    texts = [extract_text_from_pdf(p) for p in pdf_paths]

    resumes = []
    for text in texts:
        name = extract_name(text)
        email = extract_email(text)

        resumes.append({
            "name": name,
            "email": email,
            "phone": extract_contact_number(text),
            "education": extract_education(text),
            "raw_text": text
        })
        
    skill_inputs = [
        {
            "text": r["raw_text"],
            "name": r["name"],
            "email": r["email"]
        }
        for r in resumes
    ]

    skills_batch = extract_skills_batch(skill_inputs)
    for r, skills in zip(resumes, skills_batch):
        r["skills"] = skills

    return resumes