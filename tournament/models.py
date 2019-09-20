from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Organizer(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    id_card = models.CharField(max_length=10, null=True, blank=True, unique=True)
    first_phone = models.CharField(max_length=13)
    second_phone = models.CharField(max_length=13, blank=True, null=True)