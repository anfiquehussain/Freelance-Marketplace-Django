# Generated by Django 4.2.4 on 2023-08-28 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Services', '0006_remove_overview_title_overview_titleoverview'),
    ]

    operations = [
        migrations.AlterField(
            model_name='overview',
            name='titleOverview',
            field=models.CharField(max_length=100),
        ),
    ]
