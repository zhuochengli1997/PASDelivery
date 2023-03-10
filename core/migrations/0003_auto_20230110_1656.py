# Generated by Django 3.2 on 2023-01-10 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_job_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='delivered_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='delivery_photo',
            field=models.ImageField(blank=True, null=True, upload_to='job/pickup_photos/'),
        ),
        migrations.AddField(
            model_name='job',
            name='pickedup_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='pickup_photo',
            field=models.ImageField(blank=True, null=True, upload_to='job/pickup_photos/'),
        ),
    ]
