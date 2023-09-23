from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import MyTokenObtainPairSerializer, SignupSerializer


@api_view(["GET"])
def hello(request):
    return Response({"message": "Hello, world!"})


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["POST"])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            return Response(
                {
                    "user": SignupSerializer(user, context=serializer.data).data,
                    "message": "User created successfully",
                }
            )
    return Response(
        {"message": "User not created", "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )
