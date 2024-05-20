from django.db import migrations


def create_skills(apps, schema_editor):
    Skill = apps.get_model('Home', 'Skill')
    freelancer_skills = [
        "HTML/CSS",
        "JavaScript",
        "Front-end Frameworks",
        "Back-end Development",
        "Responsive Design",
        "Graphic Design",
        "UX/UI Design",
        "Adobe Creative Suite",
        "Typography",
        "Branding",
        "Video Editing Software",
        "Motion Graphics",
        "Storyboarding",
        "Color Correction",
        "Audio Editing",
        "Social Media Marketing",
        "Search Engine Optimization (SEO)",
        "Data Analysis",
        "Project Management",
        "Customer Service",
        "Sales",
        "Market Research",
        "Photography",
        "Illustration",
        "Animation",
        "Game Development",
        "Virtual Reality (VR)",
        "Augmented Reality (AR)",
        "Machine Learning",
        "Artificial Intelligence (AI)",
        "Natural Language Processing (NLP)",
        "Blockchain Development",
        "Cryptocurrency",
        "Cybersecurity",
        "Network Administration",
        "Database Management",
        "Cloud Computing",
        "DevOps",
        "UI Automation",
        "Quality Assurance (QA)",
        "Agile Methodology",
        "Scrum Framework",
        "Kanban Method",
        "Lean Manufacturing",
        "Six Sigma",
        "Financial Analysis",
        "Investment Management",
        "Tax Preparation",
        "Legal Research",
        "Medical Transcription"
    ]
    for skill_name in freelancer_skills:
        Skill.objects.create(name=skill_name)


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),  # Update with your previous migration name
    ]

    operations = [
        migrations.RunPython(create_skills),
    ]
