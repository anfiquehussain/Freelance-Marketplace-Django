# Generated by Django 4.2.4 on 2023-09-23 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0006_rename_status_order_status1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='status1',
            new_name='status',
        ),
    ]
