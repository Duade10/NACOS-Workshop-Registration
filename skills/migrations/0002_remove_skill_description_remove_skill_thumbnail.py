# Generated by Django 4.1.6 on 2023-02-09 00:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("skills", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="skill",
            name="description",
        ),
        migrations.RemoveField(
            model_name="skill",
            name="thumbnail",
        ),
    ]