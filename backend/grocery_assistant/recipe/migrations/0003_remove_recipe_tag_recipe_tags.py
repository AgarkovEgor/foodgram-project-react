# Generated by Django 4.2 on 2023-04-27 16:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("recipe", "0002_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="recipe",
            name="tag",
        ),
        migrations.AddField(
            model_name="recipe",
            name="tags",
            field=models.ManyToManyField(related_name="recipes", to="recipe.tag"),
        ),
    ]
