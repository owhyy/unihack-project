from datetime import timedelta
from django.contrib.auth import authenticate, login
from django.contrib.gis.db.models.functions import Distance
from django.db.models import F, Sum, Count
from django.utils import timezone
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, status
from rest_framework.views import Response

from trip.utils import calculate_emissions
from trip.service import start_trip, create_user, stop_trip
from trip.models import CustomUser, Trip


class UserRegisterView(CreateAPIView):
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = CustomUser
            fields = [
                "email",
                "password",
                "first_name",
                "last_name",
                "avg_fuel_consumption",
                "fuel_type",
            ]

    serializer_class = UserSerializer

    def perform_create(self, serializer):
        create_user(**serializer.validated_data)


class TripListView(ListAPIView):
    class TripListSerializer(serializers.ModelSerializer):
        distance = serializers.SerializerMethodField()

        def get_distance(self, obj):
            return obj.distance.km

        class Meta:
            model = Trip
            fields = ["origin", "destination", "distance"]

    queryset = Trip.objects.all()
    serializer_class = TripListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(user=self.request.user)
            .annotate(distance=Distance("origin", "destination"))
        )


class TripReportView(ListAPIView):
    queryset = Trip.objects.filter(destination__isnull=False)
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        days_behind = int(request.query_params["days"])
        now = timezone.now()
        time_period = now - timedelta(days=days_behind)
        result = {}

        trips = (
            super()
            .get_queryset()
            .filter(user=user, created_at__date__gte=time_period)
            .annotate(distance=Distance("origin", "destination"))
        )
        # breakpoint()
        chart = {}

        # FIXME(ion): if days_behind == 1, make a hour-by-hour graph for today's trips

        for day in range(days_behind):
            past_date = (now - timedelta(days=day)).date()
            distance_on_past_trips = (
                trips.filter(created_at__date=past_date)
                .annotate(distance=Distance("origin", "destination"))
                .aggregate(total_distance=Sum(F("distance")))
            )["total_distance"]
            distance_on_past_trips = (
                distance_on_past_trips.km if distance_on_past_trips else 0
            )
            emissions_on_past_trips = calculate_emissions(
                user.avg_fuel_consumption, user.fuel_type, distance_on_past_trips
            )
            chart[past_date.isoformat()] = emissions_on_past_trips

        total_distance = sum(t.distance.km for t in trips)
        result["total_trips"] = len(trips)
        result["total_distance"] = round(total_distance, 2)
        result["total_emissions"] = calculate_emissions(
            user.avg_fuel_consumption, user.fuel_type, total_distance
        )
        result["trips"] = chart
        return Response(result)


class TripStartView(CreateAPIView):
    class CoordinateSerializer(serializers.Serializer):
        longitude = serializers.FloatField()
        latitude = serializers.FloatField()

        class Meta:
            fields = ["longitude", "latitude"]

    serializer_class = CoordinateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        start_trip(user=self.request.user, **serializer.validated_data)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class TripStopView(CreateAPIView):
    class CoordinateSerializer(serializers.Serializer):
        longitude = serializers.FloatField()
        latitude = serializers.FloatField()

        class Meta:
            fields = ["longitude", "latitude"]

    serializer_class = CoordinateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        trip = self.perform_create(serializer)
        distance = trip.origin.distance(trip.destination)
        return Response(
            {
                "distance": distance,
                "emissions": calculate_emissions(
                    user.avg_fuel_consumption, user.fuel_type, distance
                ),
            },
            status=status.HTTP_201_CREATED,
        )

    def perform_create(self, serializer):
        return stop_trip(user=self.request.user, **serializer.validated_data)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
