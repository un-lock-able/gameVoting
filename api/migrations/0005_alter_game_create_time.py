# Generated by Django 5.0.2 on 2024-02-17 08:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0004_remove_game_create_date_game_create_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="create_time",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]