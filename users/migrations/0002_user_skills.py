# Generated by Django 4.1.6 on 2023-02-09 00:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("skills", "0002_remove_skill_description_remove_skill_thumbnail"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="skills",
            field=models.ManyToManyField(related_name="users", to="skills.skill"),
        ),
    ]
