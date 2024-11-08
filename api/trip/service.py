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


def create_trip(user: CustomUser, **kwargs):
    Trip.objects.create(user=user, **kwargs)
