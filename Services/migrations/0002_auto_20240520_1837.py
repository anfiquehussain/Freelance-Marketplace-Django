from django.db import migrations


def populate_categories(apps, schema_editor):
    Category = apps.get_model('Services', 'Category')
    freelancing_categories = [
        "Blog writing",
        "Copyediting",
        "Technical writing",
        "Language translation",
        "Scriptwriting",
        "Ghostwriting",
        "Resume/CV writing",
        "Legal writing",
        "Academic writing",
        "Proofreading",
        "Voiceover",
        "Whiteboard animation",
        "Logo design",
        "Illustration",
        "Infographic design",
        "Packaging design",
        "3D modeling",
        "Video editing",
        "Audio editing",
        "Social media management",
        "Content strategy",
        "Social media content creation",
        "Email automation",
        "Lead generation",
        "Web development",
        "Mobile app development",
        "Game development",
        "Database administration",
        "Network administration",
        "Cybersecurity",
        "Cloud computing",
        "WordPress customization",
        "Shopify development",
        "Magento development",
        "Customer service",
        "Order processing",
        'UI/UX Design',
        "Market research",
        "Financial modeling",
        "Business consulting",
        "Human resources consulting",
        "Supply chain consulting",
        "Product management",
        "Healthcare consulting",
        "Environmental consulting",
        "Political consulting"
    ]
    for category_name in freelancing_categories:
        Category.objects.create(name=category_name)


class Migration(migrations.Migration):

    dependencies = [
        ('Services', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_categories),
    ]
