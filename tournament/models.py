from django.db import models
from django.contrib.auth import get_user_model
from core.models import City


class Organizer(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    id_card = models.CharField(max_length=10,
                               null=True, blank=True, unique=True)
    first_phone = models.CharField(max_length=13)
    second_phone = models.CharField(max_length=13, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


def custom_tournament_upload_to(instance, filename):
    try:
        old_instance = Tournament.objects.get(pk=instance.pk)
    except Tournament.DoesNotExist:
        old_instance = None
    if old_instance is not None:
        old_instance.image.delete()
    return 'tournaments/' + filename


class Tournament(models.Model):
    STATE_CONFIGURING, STATE_PUBLISHED, \
        STATE_IN_PROGRESS, STATE_FINISHED = "CONFIGURING", "PUBLISHED", \
                                            "IN_PROGRESS", 'FINISHED'
    STATE_CHOICES = (
        (STATE_CONFIGURING, "Configurando"),
        (STATE_PUBLISHED, "Publicado"),
        (STATE_IN_PROGRESS, "En progreso"),
        (STATE_FINISHED, "Finalizado")
    )
    city = models.ForeignKey(City, on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    start_at = models.DateTimeField()
    state = models.CharField(max_length=15, choices=STATE_CHOICES)
    cost = models.DecimalField(max_digits=10, decimal_places=3)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    address = models.CharField(max_length=255)
    reference = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=custom_tournament_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrganizerTournament(models.Model):
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)