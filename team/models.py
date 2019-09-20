from django.db import models
from django.contrib.auth import get_user_model
from core.models import City


class Manager(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    id_card = models.CharField(max_length=10,
                               null=True, blank=True, unique=True)
    first_phone = models.CharField(max_length=13)
    second_phone = models.CharField(max_length=13, blank=True, null=True)
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
    STATE_PRE_REGISTERED, STATE_REGISTERED, \
        STATE_CONFIRMED = "PRE_REGISTERED", "REGISTERED", "CONFIRMED",
    STATE_CHOICES = (
        (STATE_PRE_REGISTERED, "Pre-Registrado"),
        (STATE_REGISTERED, "Registrado"),
        (STATE_CONFIRMED, "Confirmado")
    )
    manager = models.ForeignKey(Manager, on_delete=models.PROTECT)
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    name = models.CharField(max_length=40)
    logo = models.ImageField(upload_to=custom_team_upload_to)
    state = models.CharField(max_length=15, choices=STATE_CHOICES)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
