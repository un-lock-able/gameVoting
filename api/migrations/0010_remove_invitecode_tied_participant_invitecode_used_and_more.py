# Generated by Django 5.0.2 on 2024-02-17 12:32

import api.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0009_alter_invitecode_code"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="invitecode",
            name="tied_participant",
        ),
        migrations.AddField(
            model_name="invitecode",
            name="used",
            field=models.BooleanField(default=False, verbose_name="Used"),
        ),
        migrations.AddField(
            model_name="participant",
            name="register_code",
            field=models.ForeignKey(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                to="api.invitecode",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="invitecode",
            name="code",
            field=models.CharField(
                default=api.models.gen_invite_code,
                editable=False,
                max_length=20,
                verbose_name="Invite code",
            ),
        ),
    ]
