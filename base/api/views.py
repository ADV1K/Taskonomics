from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import MyTokenObtainPairSerializer, SignupSerializer


@api_view(["GET"])
def hello(request):
    return Response({"message": "Hello, world!"})


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SignupView(APIView):
    serializer_class = SignupSerializer

    @staticmethod
    def post(request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(
                    {
                        "message": "User created successfully",
                        "user": SignupSerializer(user, context=serializer.data).data,
                    }
                )
        return Response(
            {"message": "User not created", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
