# Generated by Django 4.2.4 on 2023-09-14 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order_requirements',
            name='order',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Orders.order'),
        ),
    ]
