from django.db import models
from django.contrib.auth import get_user_model
from core.models import City, WeekDay
from team.models import Team
from django.utils.timezone import now


class Organizer(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
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
    cost = models.DecimalField(max_digits=5, decimal_places=2)
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


class TournamentTeam(models.Model):
    STATE_REGISTERED, STATE_ENROLLED, \
        STATE_CONFIRMED = "REGISTERED", "ENROLLED", "CONFIRMED",
    STATE_CHOICES = (
        (STATE_REGISTERED, "Registradp"),
        (STATE_ENROLLED, "Inscrito"),
        (STATE_CONFIRMED, "Confirmado")
    )
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(default=now)
    team_state = models.CharField(max_length=15, choices=STATE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TournamentWeekDay(models.Model):
    tournament_team = models.ForeignKey(TournamentTeam, on_delete=models.CASCADE)
    game_day = models.ForeignKey(WeekDay, on_delete=models.PROTECT)
    playable = models.BooleanField(default=False)
    start_time = models.TimeField()
    end_time = models.TimeField()


def custom_payment_upload_to(instance, filename):
    try:
        old_instance = Payment.objects.get(pk=instance.pk)
    except Payment.DoesNotExist:
        old_instance = None
    if old_instance is not None:
        old_instance.image.delete()
    return 'payments/' + filename


class Payment(models.Model):
    tournament_team = models.ForeignKey(TournamentTeam, on_delete=models.CASCADE)
    payment_at = models.DateTimeField(default=now)
    value = models.DecimalField(max_digits=5, decimal_places=2)
    detail = models.TextField()
    voucher = models.ImageField(upload_to=custom_payment_upload_to, blank=True, null=True)