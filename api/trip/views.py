from datetime import timedelta
from django.contrib.auth import authenticate, login
from django.contrib.gis.db.models.functions import Distance
from django.db.models import Sum
from django.utils import timezone
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, status
from rest_framework.views import Response

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
    class TripListSerializer(serializers.ModelSerializer):
        distance_past_week = serializers.SerializerMethodField()

        def get_distance_past_week(self, obj):
            return obj.distance_past_week.km

        class Meta:
            model = Trip
            fields = ["distance_past_week"]

    serializer_class = TripListSerializer
    queryset = Trip.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        past_week = timezone.now() - timedelta(days=7)
        return (
            super()
            .get_queryset()
            .filter(user=self.request.user, created_at__gte=past_week)
            .annotate(distance=Distance("origin", "destination"))
            .annotate(distance_past_week=Sum("distance"))
        )


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
