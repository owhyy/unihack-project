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
from trip.service import create_trip, create_user
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


class UserLoginView(CreateAPIView):
    class LoginSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

        class Meta:
            fields = [
                "email",
                "password",
            ]

    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if user is None:
            return Response(
                {"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
            )

        login(request, user)

        return Response(serializer.data, status=status.HTTP_200_OK)


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
    queryset = Trip.objects.all()
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
            .filter(user=user, created_at__gte=time_period)
            .annotate(distance=Distance("origin", "destination"))
        )
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
        result["total_distance"] = total_distance
        result["total_emissions"] = calculate_emissions(
            user.avg_fuel_consumption, user.fuel_type, total_distance
        )
        result["trips"] = chart
        return Response(result)


class TripCreateView(CreateAPIView):
    class CreateTripSerializer(serializers.ModelSerializer):
        class Meta:
            model = Trip
            fields = ["origin", "destination"]

    serializer_class = CreateTripSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        create_trip(user=self.request.user, **serializer.validated_data)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
