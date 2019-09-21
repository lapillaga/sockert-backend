from django.contrib import admin
from core.models import WeekDay, City, Province


@admin.register(WeekDay)
class WeekDayAdmin(admin.ModelAdmin):
    pass


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    pass


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    pass

