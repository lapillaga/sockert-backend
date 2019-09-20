from django.db import models


# Create your models here.
class Province(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class City(models.Model):
    province = models.ForeignKey(Province, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
