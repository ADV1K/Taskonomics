from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from base.models import Project, Task

from .serializers import (
    MyTokenObtainPairSerializer,
    ProjectSerializer,
    TaskSerializer,
    UserSerializer,
)


class IsProjectOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsTaskOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return obj.creator == request.user


class HeartbeatView(APIView):
    @staticmethod
    def get(request):
        return Response({"status": "ok"})


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SignupView(APIView):
    serializer_class = UserSerializer

    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(
                    {
                        "message": "User created successfully",
                        "user": UserSerializer(user, context=serializer.data).data,
                    }
                )
        return Response(
            {"message": "User not created", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        timezone.activate(self.request.user.timezone)
        queryset = Task.objects.filter(creator=self.request.user)
        assignee = self.request.query_params.get("assignee", None)
        reviewer = self.request.query_params.get("reviewer", None)

        if assignee is not None:
            queryset = queryset.filter(assignee=assignee)
        if reviewer is not None:
            # reviewers is a many-to-many field, so we need to use the __ syntax
            queryset = queryset.filter(reviewers__id=reviewer)

        return queryset.all()


class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsTaskOwner]

    def get_queryset(self):
        timezone.activate(self.request.user.timezone)
        return Task.objects.filter(creator=self.request.user).all()


class ProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        timezone.activate(self.request.user.timezone)
        return Project.objects.filter(owner=self.request.user).all()


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    permission_classes = [IsProjectOwner]

    def get_queryset(self):
        timezone.activate(self.request.user.timezone)
        return Project.objects.filter(owner=self.request.user).all()
