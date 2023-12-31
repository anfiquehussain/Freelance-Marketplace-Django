# Generated by Django 4.2.4 on 2023-09-24 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Orders', '0012_alter_order_requirements_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_status', models.CharField(choices=[('pending', 'Pending'), ('in_transit', 'In Transit'), ('delivered', 'Delivered'), ('failed', 'Failed')], default='pending', max_length=20)),
                ('delivery_notes', models.TextField(blank=True, null=True)),
                ('delivery_modifcation_note', models.TextField(blank=True, null=True)),
                ('order_delivered_date', models.DateField(blank=True, null=True)),
                ('delivery_file', models.FileField(blank=True, null=True, upload_to='delivery_files/')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Orders.order')),
            ],
        ),
    ]
