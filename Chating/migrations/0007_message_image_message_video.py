# Generated by Django 4.2.4 on 2023-10-02 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chating', '0006_remove_message_image_remove_message_video_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='message_images/'),
        ),
        migrations.AddField(
            model_name='message',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='message_videos/'),
        ),
    ]
