# Generated by Django 4.2.4 on 2023-08-14 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0007_rename_name1_skill_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='skills',
            field=models.ManyToManyField(default=['db', 'dn'], related_name='user_profiles', to='Home.skill'),
        ),
    ]
