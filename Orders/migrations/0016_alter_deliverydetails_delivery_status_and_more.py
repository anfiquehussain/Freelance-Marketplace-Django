# Generated by Django 4.2.4 on 2023-09-24 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0015_alter_deliverydetails_delivery_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverydetails',
            name='delivery_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('in_transit', 'In Transit'), ('return', 'Return'), ('delivered', 'Delivered'), ('failed', 'Failed')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('cancelled', 'Cancelled'), ('expired', 'Expired'), ('return', 'Return'), ('delivered', 'Delivered'), ('completed', 'Completed')], default='pending', max_length=20),
        ),
    ]
