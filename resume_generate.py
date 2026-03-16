from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
import random
from pathlib import Path


styles = getSampleStyleSheet()


names = [
    "John Smith", "Alice Johnson", "Michael Brown", "Emma Davis", "Daniel Wilson",
    "Sophia Taylor", "James Anderson", "Olivia Thomas", "William Moore", "Ava Martin",
    "Lucas Clark", "Mia Rodriguez", "Ethan Walker", "Isabella Hall", "Noah Allen",
    "Charlotte Young", "Liam Hernandez", "Amelia King", "Benjamin Wright", "Harper Scott",
    "Alexander Green", "Ella Adams", "Matthew Nelson", "Scarlett Carter", "David Mitchell",
    "Emily Perez", "Joseph Roberts", "Abigail Turner", "Samuel Phillips", "Grace Campbell",
    "Christopher Parker", "Chloe Evans", "Andrew Edwards", "Victoria Collins", "Joshua Stewart",
    "Zoe Sanchez", "Nathan Morris", "Lily Rogers", "Ryan Reed", "Hannah Cook",
    "Brandon Morgan", "Natalie Bell", "Justin Murphy", "Leah Bailey", "Kevin Rivera",
    "Audrey Cooper", "Dylan Richardson", "Madison Cox", "Aaron Howard", "Brooklyn Ward",
    "Tyler Torres", "Savannah Peterson", "Jordan Gray", "Claire Ramirez", "Logan James",
    "Evelyn Watson", "Connor Brooks", "Lucy Kelly", "Adam Sanders", "Aria Price"
]

companies = [
    "ABC Tech", "DataCorp", "VisionTech", "Future Systems", "Creative Studio",
    "MarketEdge", "FinanceHub", "HealthPlus", "EduSmart", "Global Solutions",
    "NextWave AI", "BrightPath Consulting", "NovaSoft", "GreenField Analytics",
    "BluePeak Technologies", "Insight Dynamics", "Vertex Solutions",
    "Quantum Labs", "SilverLine Systems", "Pioneer Innovations",
    "Skyline Software", "DeepLogic Systems", "CloudNova", "SmartGrid Technologies",
    "DataSphere Analytics", "NextGen Robotics", "AlphaCore Systems",
    "Digital Horizon", "FusionTech Labs", "PrimeEdge Solutions",
    "InnovateX", "CyberVision", "LogicBridge", "CoreData Systems",
    "Elevate Software", "BrightCode Technologies", "PixelWave Studios",
    "Vector AI", "Orion Technologies", "BlueOrbit Systems",
    "Zenith Digital", "SparkFlow Labs", "Atlas Computing",
    "Nimbus Technologies", "Stratos Solutions", "OptimaSoft",
    "Hyperion Systems", "EdgePoint Analytics", "Catalyst Labs",
    "InsightForge", "QuantumEdge", "TerraLogic", "Pulse Technologies",
    "VertexAI", "NovaCore Systems", "DeepStream Analytics",
    "Synapse Solutions", "AuroraTech", "IronPeak Software"
]

universities = [
    "University of Example", "Global Institute", "Tech University", "Innovation University",
    "City College", "National Institute of Technology", "Metropolitan University",
    "International Science University", "Central State University",
    "Advanced Technology Institute", "Northbridge University", "Westlake College",
    "Summit Technical University", "Evergreen University",
    "Brighton Institute of Technology", "Pacific State University",
    "Grand Valley University", "Capital City University",
    "Redwood Institute", "Horizon University",
    "Midland University", "Riverdale College", "Highland Institute of Technology",
    "Silver Oak University", "Eastern Technical University", "Western State College",
    "Northshore University", "Southgate Institute", "Crescent City University",
    "Liberty Technical College", "Frontier University", "Oakridge Institute",
    "Lakeview University", "Pinecrest College", "Stonebridge University",
    "Maplewood Institute", "Brookfield University", "Sunrise Technical University",
    "Clearwater College", "Hillcrest University", "Lakeside Institute",
    "Golden Valley University", "Blue Ridge Technical University",
    "Harbor City University", "Prairie State College", "Skyline Institute",
    "Unity University", "New Horizons College", "Summit Ridge University",
    "Bridgewater Institute", "North Valley University", "Eastwood College",
    "Greenwood University", "Westfield Institute", "Ironwood University",
    "Granite State University", "Cedar Hill College", "Crystal Lake University"
]

profiles = {

    "software_engineer": {
        "title": "Software Engineer",
        "degree": "Bachelor of Computer Science",
        "skills": [
            "Python", "Java", "C++", "SQL", "Docker", "Kubernetes", "Git",
            "REST APIs", "Microservices", "Linux", "System Design", "CI/CD"
        ]
    },

    "data_scientist": {
        "title": "Data Scientist",
        "degree": "Master of Data Science",
        "skills": [
            "Python", "Machine Learning", "Pandas", "NumPy", "TensorFlow",
            "PyTorch", "Statistics", "Data Visualization", "Scikit-learn",
            "Deep Learning", "Feature Engineering", "SQL"
        ]
    },

    "marketing_specialist": {
        "title": "Marketing Specialist",
        "degree": "Bachelor of Marketing",
        "skills": [
            "SEO", "Content Marketing", "Google Analytics", "Social Media",
            "Brand Strategy", "Email Marketing", "Market Research",
            "Campaign Management", "Copywriting", "Digital Advertising"
        ]
    },

    "finance_analyst": {
        "title": "Financial Analyst",
        "degree": "Bachelor of Finance",
        "skills": [
            "Financial Modeling", "Excel", "Accounting", "Risk Analysis",
            "Forecasting", "Data Analysis", "Investment Analysis",
            "Budget Planning", "Corporate Finance", "Valuation"
        ]
    },

    "graphic_designer": {
        "title": "Graphic Designer",
        "degree": "Bachelor of Design",
        "skills": [
            "Photoshop", "Illustrator", "UI Design", "Typography",
            "Branding", "Figma", "Layout Design", "Color Theory",
            "Visual Storytelling", "Adobe Creative Suite"
        ]
    },

    "devops_engineer": {
        "title": "DevOps Engineer",
        "degree": "Bachelor of Computer Engineering",
        "skills": [
            "Docker", "Kubernetes", "CI/CD", "AWS", "Terraform",
            "Linux", "Monitoring", "Prometheus", "Grafana", "Ansible"
        ]
    },

    "product_manager": {
        "title": "Product Manager",
        "degree": "MBA",
        "skills": [
            "Product Strategy", "Roadmapping", "Agile", "Scrum",
            "Market Research", "User Stories", "Stakeholder Management",
            "Data Analysis", "Product Lifecycle", "A/B Testing"
        ]
    },

    "business_analyst": {
        "title": "Business Analyst",
        "degree": "Bachelor of Business Administration",
        "skills": [
            "Data Analysis", "SQL", "Excel", "Process Modeling",
            "Stakeholder Communication", "Requirements Gathering",
            "Business Intelligence", "Tableau", "Power BI", "Reporting"
        ]
    },

    "cybersecurity_specialist": {
        "title": "Cybersecurity Specialist",
        "degree": "Bachelor of Cybersecurity",
        "skills": [
            "Network Security", "Penetration Testing", "SIEM",
            "Vulnerability Assessment", "Incident Response",
            "Cryptography", "Firewalls", "Security Auditing",
            "Threat Analysis", "Ethical Hacking"
        ]
    },

    "machine_learning_engineer": {
        "title": "Machine Learning Engineer",
        "degree": "Master of Artificial Intelligence",
        "skills": [
            "Python", "PyTorch", "TensorFlow", "Deep Learning",
            "Model Deployment", "Feature Engineering",
            "Computer Vision", "NLP", "Data Pipelines", "MLOps"
        ]
    },

    "ui_ux_designer": {
        "title": "UI/UX Designer",
        "degree": "Bachelor of Interaction Design",
        "skills": [
            "Figma", "Wireframing", "Prototyping", "User Research",
            "Usability Testing", "Interaction Design",
            "Design Systems", "User Journey Mapping", "Accessibility"
        ]
    },

    "data_engineer": {
        "title": "Data Engineer",
        "degree": "Bachelor of Computer Engineering",
        "skills": [
            "Python", "SQL", "Spark", "Kafka", "ETL Pipelines",
            "Data Warehousing", "Airflow", "Hadoop", "Cloud Data Platforms"
        ]
    }

}

def resume_generator(num=10, output_dir="./resumes"):

    Path(output_dir).mkdir(exist_ok=True)

    for i in range(num):

        name = random.choice(names)
        company = random.choice(companies)
        university = random.choice(universities)

        profile = random.choice(list(profiles.values()))

        title = profile["title"]
        degree = profile["degree"]
        selected_skills = random.sample(profile["skills"], 4)

        file_path = f"{output_dir}/resume_{i + 1}.pdf"

        story = []

        # Header
        story.append(Paragraph(f"<b>{name}</b>", styles['Title']))
        story.append(Paragraph(
            f"Email: {name.lower().replace(' ', '')}@email.com | Phone: +1 555 12{i % 10} 456{i % 10}",
            styles['Normal']))
        story.append(Spacer(1, 12))

        # Summary
        story.append(
            Paragraph("<b>Professional Summary</b>", styles['Heading2']))
        story.append(Paragraph(
            f"Experienced {title.lower()} with strong problem-solving skills and experience in industry projects.",
            styles['Normal']))
        story.append(Spacer(1, 12))

        # Skills
        story.append(Paragraph("<b>Skills</b>", styles['Heading2']))

        skills_data = [
            ["Core Skills", ", ".join(selected_skills[:2])],
            ["Tools", ", ".join(selected_skills[2:])]
        ]

        table = Table(skills_data, colWidths=[5 * cm, 10 * cm])
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

    print(f"{num} resumes generated in '{output_dir}' folder.")
