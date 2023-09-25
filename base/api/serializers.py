import pytz
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from base.models import Project, Task, User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        print(user.first_name, user.email)
        token["name"] = user.first_name
        token["email"] = user.email

        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "timezone", "first_name", "last_name")
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "timezone": {"required": True},
            "date_joined": {"read_only": True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    @staticmethod
    def validate_timezone(value):
        if value not in pytz.all_timezones:
            raise serializers.ValidationError("Invalid timezone")
        return value


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=255, required=True)
    creator = serializers.HiddenField(default=serializers.CurrentUserDefault())
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    reviewers = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    due_date = serializers.DateTimeField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        reviewers = validated_data.pop("reviewers")
        task = Task.objects.create(**validated_data)
        task.reviewers.add(*(r.id for r in reviewers))
        return task

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance

    def validate_project(self, value):
        if value.owner != self.context["request"].user:
            raise serializers.ValidationError("You are not the owner of this project")
        return value


class ProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, required=False)
    name = serializers.CharField(max_length=255)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
