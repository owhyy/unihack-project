from django.db import models
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
    
