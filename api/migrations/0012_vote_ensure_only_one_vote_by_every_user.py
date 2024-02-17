# Generated by Django 5.0.2 on 2024-02-17 16:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0011_alter_invitecode_code"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="vote",
            constraint=models.UniqueConstraint(
                fields=("voting_user", "voting_character"),
                name="Ensure only one vote by every user",
            ),
        ),
    ]
