from . import models
from rest_framework import views
from rest_framework import status
from . import serializers
from rest_framework import permissions
from rest_framework_simplejwt import authentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer


class User(views.APIView):
    def get(self, request):
        users = models.User.objects.all().order_by("-created_at")
        serializer = serializers.UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = serializers.UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(views.APIView):
    def get(self, request, pk):
        user = models.User.objects.get(id=pk)
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = models.User.objects.get(id=pk)
        data = request.data
        serializer = serializers.UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user = models.User.objects.get(id=pk)
        except models.User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({"success": True}, status=status.HTTP_200_OK)


class ProfileView(views.APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response(serializer.errors, status=400)
