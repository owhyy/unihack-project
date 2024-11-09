from trip.models import CustomUser

VEHICLE_EMISSION_FACTOR = 3000
VEHICLE_LIFESPAN_KM = 150000
INFRASTRUCTURE_FACTOR = 0.05

PETROL_EMISSION_FACTOR = 2.31
DIESEL_EMISSION_FACTOR = 2.68
DIRECT_EMISSION_FACTORS = {
    CustomUser.FuelType.GASOLINE: 2.31,
    CustomUser.FuelType.DIESEL: 2.68,
}
INDIRECT_EMISSION_FACTORS = {
    CustomUser.FuelType.GASOLINE: 0.15,
    CustomUser.FuelType.DIESEL: 0.18,
}


def calculate_emissions(
    liters_per_100km: float, fuel_type: CustomUser.FuelType, distance: int
) -> float:
    direct_emissions = (distance * liters_per_100km / 100) * DIRECT_EMISSION_FACTORS[
        fuel_type
    ]

    indirect_emissions = (
        distance * liters_per_100km / 100
    ) * INDIRECT_EMISSION_FACTORS[fuel_type]

    vehicle_emissions = (VEHICLE_EMISSION_FACTOR / VEHICLE_LIFESPAN_KM) * distance

    infrastructure_emissions = distance * INFRASTRUCTURE_FACTOR

    total_emissions = (
        direct_emissions
        + indirect_emissions
        + vehicle_emissions
        + infrastructure_emissions
    )

    return total_emissions
