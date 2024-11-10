from django.contrib.gis.db.models.fields import Point
from django.utils import timezone
from django.contrib.auth.models import make_password
from trip.models import CustomUser, Trip


def create_user(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    avg_fuel_consumption: int,
    fuel_type: CustomUser.FuelType,
) -> CustomUser:
    email = CustomUser.objects.normalize_email(email)
    user = CustomUser(
        email=email,
        first_name=first_name,
        last_name=last_name,
        avg_fuel_consumption=avg_fuel_consumption,
        fuel_type=fuel_type,
        is_staff=False,
        is_active=True,
    )
    user.password = make_password(password)
    user.save()
    return user

# FIXME(ion): ideally we'd have a better way to handle the case where a user tries to start a new trip if one is already started...
def start_trip(user: CustomUser, longitude: float, latitude: float):
    point = Point(longitude, latitude)
    user.trips.filter(stopped_at__isnull=True).update(destination=point, stopped_at=timezone.now())
    
    Trip.objects.create(user=user, origin=point)


def stop_trip(user: CustomUser, longitude: float, latitude: float):
    point = Point(longitude, latitude)    
    user.trips.filter(stopped_at__isnull=True).update(destination=point, stopped_at=timezone.now())
    return user.trips.latest("id")
