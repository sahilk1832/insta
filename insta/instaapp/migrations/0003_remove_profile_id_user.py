# Generated by Django 5.0.7 on 2024-08-02 13:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instaapp', '0002_profile_birth_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='id_user',
        ),
    ]
