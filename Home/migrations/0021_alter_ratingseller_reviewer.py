# Generated by Django 4.2.4 on 2024-01-06 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0020_ratingseller_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ratingseller',
            name='reviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviewer', to='Home.userprofile'),
        ),
    ]
