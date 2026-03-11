import re
from pdfminer.high_level import extract_text
import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")


def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)


def extract_contact_number_from_resume(text):
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    return match.group() if match else None


def extract_email_from_resume(text):
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    return match.group() if match else None


def extract_skills_from_resume(text, skills_list):

    doc = nlp(text)

    skills = []

    for sent in doc.sents:

        sentence_text = sent.text

        for skill in skills_list:

            pattern = r"\b{}\b".format(re.escape(skill))

            if re.search(pattern, sentence_text, re.IGNORECASE):

                skills.append({
                    "skill": skill,
                    "context": sentence_text.strip()
                })

    return skills


def extract_education_from_resume(text):
    pattern = r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.\w+|\bBachelor(?:'s)?|\bMaster(?:'s)?|\bPh\.D)\s(?:\w+\s)*\w+"
    return re.findall(pattern, text)


def extract_name(resume_text):

    matcher = Matcher(nlp.vocab)

    patterns = [
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}],
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}],
        [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]
    ]

    matcher.add("NAME", patterns)

    doc = nlp(resume_text)
    matches = matcher(doc)

    for match_id, start, end in matches:
        span = doc[start:end]
        return span.text

    return None


# MAIN PARSER FUNCTION
def parse_resume(pdf_path, skills_list):

    text = extract_text_from_pdf(pdf_path)

    result = {
        "name": extract_name(text),
        "email": extract_email_from_resume(text),
        "phone": extract_contact_number_from_resume(text),
        "skills": extract_skills_from_resume(text, skills_list),
        "education": extract_education_from_resume(text),
        "raw_text": text
    }

    return result


if __name__ == "__main__":
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

    for i in range(10):

        resume_path = f".\\resume_{i+1}.pdf"

        print("Resume:", resume_path)

        data = parse_resume(resume_path, skills_list)

        print("Name:", data["name"])
        print("Email:", data["email"])
        print("Phone:", data["phone"])
        print("Skills:", [s["skill"] for s in data["skills"]])
        print("Education:", data["education"])
    