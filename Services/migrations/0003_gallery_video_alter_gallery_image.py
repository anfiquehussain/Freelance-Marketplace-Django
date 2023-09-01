# Generated by Django 4.2.4 on 2023-08-27 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Services', '0002_remove_gallery_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='video',
            field=models.FileField(default='video', upload_to='videos/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gallery',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
