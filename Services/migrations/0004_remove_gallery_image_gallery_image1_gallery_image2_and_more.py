# Generated by Django 4.2.4 on 2023-08-27 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Services', '0003_gallery_video_alter_gallery_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallery',
            name='image',
        ),
        migrations.AddField(
            model_name='gallery',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='image/'),
        ),
        migrations.AddField(
            model_name='gallery',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='image/'),
        ),
        migrations.AddField(
            model_name='gallery',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='image/'),
        ),
        migrations.AlterField(
            model_name='extraservice',
            name='title',
            field=models.CharField(default='2', max_length=100),
        ),
        migrations.AlterField(
            model_name='gallery',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos/'),
        ),
    ]
