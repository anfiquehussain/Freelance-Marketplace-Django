# Generated by Django 4.2.4 on 2023-09-24 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0013_deliverydetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverydetails',
            name='delivery_notes',
            field=models.TextField(default='delivery_notes'),
            preserve_default=False,
        ),
    ]
