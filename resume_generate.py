from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
import random

styles = getSampleStyleSheet()

names = [
    "John Smith", "Alice Johnson", "Michael Brown", "Emma Davis", "Daniel Wilson",
    "Sophia Taylor", "James Anderson", "Olivia Thomas", "William Moore", "Ava Martin",
    "Lucas Clark", "Mia Rodriguez", "Ethan Walker", "Isabella Hall", "Noah Allen",
    "Charlotte Young", "Liam Hernandez", "Amelia King", "Benjamin Wright", "Harper Scott"
]

companies = [
    "ABC Tech", "DataCorp", "VisionTech", "Future Systems", "Creative Studio",
    "MarketEdge", "FinanceHub", "HealthPlus", "EduSmart", "Global Solutions",
    "NextWave AI", "BrightPath Consulting", "NovaSoft", "GreenField Analytics",
    "BluePeak Technologies", "Insight Dynamics", "Vertex Solutions",
    "Quantum Labs", "SilverLine Systems", "Pioneer Innovations"
]

universities = [
    "University of Example",
    "Global Institute",
    "Tech University",
    "Innovation University",
    "City College",
    "National Institute of Technology",
    "Metropolitan University",
    "International Science University",
    "Central State University",
    "Advanced Technology Institute",
    "Northbridge University",
    "Westlake College",
    "Summit Technical University",
    "Evergreen University",
    "Brighton Institute of Technology",
    "Pacific State University",
    "Grand Valley University",
    "Capital City University",
    "Redwood Institute",
    "Horizon University"
]

# Different professional profiles
profiles = {

    "software_engineer": {
        "title": "Software Engineer",
        "degree": "Bachelor of Computer Science",
        "skills": ["Python", "Java", "SQL", "Docker", "Git", "REST APIs"]
    },

    "data_scientist": {
        "title": "Data Scientist",
        "degree": "Master of Data Science",
        "skills": ["Python", "Machine Learning", "Pandas", "NumPy", "TensorFlow", "Statistics"]
    },

    "marketing_specialist": {
        "title": "Marketing Specialist",
        "degree": "Bachelor of Marketing",
        "skills": ["SEO", "Content Marketing", "Google Analytics", "Social Media", "Brand Strategy", "Email Marketing"]
    },

    "finance_analyst": {
        "title": "Financial Analyst",
        "degree": "Bachelor of Finance",
        "skills": ["Financial Modeling", "Excel", "Accounting", "Risk Analysis", "Forecasting", "Data Analysis"]
    },

    "graphic_designer": {
        "title": "Graphic Designer",
        "degree": "Bachelor of Design",
        "skills": ["Photoshop", "Illustrator", "UI Design", "Typography", "Branding", "Figma"]
    }

}


selected_names = random.sample(names, 10)
selected_companies = random.sample(companies, 10)
selected_universities = random.sample(universities, 10)

for i in range(10):
    name = selected_names[i]
    company = selected_companies[i]
    university = selected_universities[i]

    profile = random.choice(list(profiles.values()))

    title = profile["title"]
    degree = profile["degree"]
    selected_skills = random.sample(profile["skills"], 4)

    file_path = f"resume_{i+1}.pdf"

    story = []

    # Header
    story.append(Paragraph(f"<b>{name}</b>", styles['Title']))
    story.append(Paragraph(
        f"Email: {name.lower().replace(' ', '')}@email.com | Phone: +1 555 12{i} 456{i}",
        styles['Normal']))
    story.append(Spacer(1, 12))

    # Summary
    story.append(Paragraph("<b>Professional Summary</b>", styles['Heading2']))
    story.append(Paragraph(
        f"Experienced {title.lower()} with strong problem-solving skills and experience "
        f"in industry projects.", styles['Normal']))
    story.append(Spacer(1, 12))

    # Skills
    story.append(Paragraph("<b>Skills</b>", styles['Heading2']))

    skills_data = [
        ["Core Skills", ", ".join(selected_skills[:2])],
        ["Tools", ", ".join(selected_skills[2:])]
    ]

    table = Table(skills_data, colWidths=[5*cm, 10*cm])
    table.setStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey)
    ])

    story.append(table)
    story.append(Spacer(1, 12))

    # Experience
    story.append(Paragraph("<b>Work Experience</b>", styles['Heading2']))
    story.append(Paragraph(
        f"<b>{title} – {company}</b> (2022–Present)", styles['Normal']))
    story.append(Paragraph(
        "- Managed professional projects\n"
        "- Collaborated with cross-functional teams\n"
        "- Improved company processes and efficiency",
        styles['Normal']))
    story.append(Spacer(1, 12))

    # Education
    story.append(Paragraph("<b>Education</b>", styles['Heading2']))
    story.append(Paragraph(
        f"{degree} – {university} (2018–2022)",
        styles['Normal']))

    doc = SimpleDocTemplate(file_path, pagesize=A4)
    doc.build(story)

print("10 diverse resumes generated.")
