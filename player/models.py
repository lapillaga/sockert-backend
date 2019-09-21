from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _


# Create your models here.
class Player(models.Model):
    GENRE_MALE, GENRE_FEMALE = "MALE", "FEMALE"
    GENRE_CHOICES = (
        (GENRE_MALE, _('Male')),
        (GENRE_FEMALE, _('Female')),
    )
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    birthday_date = models.DateField()
    gender = models.CharField(max_length=10, choices=GENRE_CHOICES)
    address = models.CharField(max_length=255)

