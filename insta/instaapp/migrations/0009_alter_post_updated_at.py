# Generated by Django 5.0.7 on 2024-08-04 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instaapp', '0008_alter_post_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
