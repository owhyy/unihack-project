from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin
from trip.models import Trip


@admin.register(Trip)
class TripAdmin(GISModelAdmin):
    list_display = ("origin", "destination")
