# Generated by Django 5.1.7 on 2025-03-29 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_pics',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
