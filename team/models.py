from django.utils.timezone import now
from django.db import models
from django.contrib.auth import get_user_model
from core.models import City
from player.models import Player


class Manager(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def custom_team_upload_to(instance, filename):
    try:
        old_instance = Team.objects.get(pk=instance.pk)
    except Team.DoesNotExist:
        old_instance = None
    if old_instance is not None:
        old_instance.image.delete()
    return 'teams/' + filename


class Team(models.Model):
    manager = models.ForeignKey(Manager, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    name = models.CharField(max_length=40)
    logo = models.ImageField(upload_to=custom_team_upload_to)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TeamPlayer(models.Model):
    STATE_REGISTERED, STATE_ENROLLED, \
        STATE_BANNED = "REGISTERED", "ENROLLED", "BANNED",
    STATE_CHOICES = (
        (STATE_REGISTERED, "Registradp"),
        (STATE_ENROLLED, "Inscrito"),
        (STATE_BANNED, "Baneado")
    )
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    player_state = models.CharField(max_length=11, choices=STATE_CHOICES)
    number = models.PositiveSmallIntegerField()
    registered_at = models.DateTimeField(default=now)