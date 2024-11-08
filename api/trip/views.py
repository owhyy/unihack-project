from django.contrib.auth import authenticate, login
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers, status
from rest_framework.views import Response

from trip.service import create_user
from trip.models import CustomUser, Trip


class RegisterUserView(CreateAPIView):
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

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        create_user(**serializer.validated_data)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class LoginUserView(CreateAPIView):
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
        class Meta:
            model = Trip
            fields = ["origin", "destination"]

    queryset = Trip.objects.all()
    serializer_class = TripListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
