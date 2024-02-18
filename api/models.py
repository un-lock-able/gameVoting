from django.db import models
from django.utils.translation import gettext_lazy
from django.utils import timezone
import random

def gen_invite_code():
    letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choice(letters) for _ in range(6)) 

# Create your models here.
class Game(models.Model):
    game_name = models.CharField(max_length=200, unique=True)
    create_time = models.DateTimeField("Created", auto_now_add=True)
    last_update_time = models.DateTimeField("Last updated", auto_now=True)

    def __str__(self):
        return self.game_name

class GameCharacter(models.Model):
    class Sex(models.TextChoices):
        MALE = "MX", gettext_lazy("Male")
        FEMALE = "FX", gettext_lazy("Female")
        __empty__ = gettext_lazy("Undefined")

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    sex = models.CharField(max_length=2, choices=Sex, default=Sex.__empty__)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["game", "name"], name="Ensure unique character name in one game")
        ]

    def __str__(self):
        return self.name


class InviteCode(models.Model):
    code = models.CharField("Invite code", max_length=20, default=gen_invite_code, editable=False, unique=True)
    used = models.BooleanField("Used", default=False)

    def __str__(self):
        return self.code


class Participant(models.Model):
    name = models.CharField(max_length=200, unique=True)
    create_time = models.DateTimeField(default=timezone.now)
    register_code = models.ForeignKey(InviteCode, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.name)


class Vote(models.Model):    
    voting_user = models.ForeignKey(Participant, on_delete=models.CASCADE)
    voting_character = models.ForeignKey(GameCharacter, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField("Last updated", auto_now=True)
    score = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["voting_user", "voting_character"], name="Ensure only one vote by every user")
        ]