# Generated by Django 4.2.4 on 2024-01-06 11:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Home', '0018_alter_ratingseller_reviewer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratingseller',
            name='reviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ratingseller',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.userprofile'),
        ),
    ]
