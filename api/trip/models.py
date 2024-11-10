from carbon.models import BaseModel

from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    class FuelType(models.TextChoices):
        DIESEL = "diesel"
        GASOLINE = "gasoline"

    email = models.EmailField(blank=True, unique=True)
    username = ""
    avg_fuel_consumption = models.PositiveIntegerField()
    fuel_type = models.CharField(choices=FuelType.choices)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Trip(BaseModel):
    origin = models.PointField()
    destination = models.PointField(null=True)

    stopped_at = models.DateTimeField(null=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="trips")
