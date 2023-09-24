import pytz
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from base.models import User


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password", "timezone", "first_name", "last_name")
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "timezone": {"required": True},
            "date_joined": {"read_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data,
            password=validated_data["password"],
            email=validated_data["email"],
        )
        return user

    @staticmethod
    def validate_timezone(value):
        if value not in pytz.all_timezones:
            raise serializers.ValidationError("Invalid timezone")
        return value


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        print(user.first_name, user.email)
        token["name"] = user.first_name
        token["email"] = user.email

        return token
