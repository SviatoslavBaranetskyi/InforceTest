from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from django.utils import timezone

from .models import Employee, Vote
from .serializers import SignUpSerializer, ProfileSerializer, VoteSerializer
from .permissions import IsOwner


class VersionedAPIView(APIView):
    def dispatch(self, request, *args, **kwargs):
        version = request.headers.get('X-App-Version', None)

        if version == '2':
            raise NotFound("Version 2 is not supported yet")

        return super().dispatch(request, *args, **kwargs)


class SignUpView(VersionedAPIView, APIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            if User.objects.filter(username=username).exists():
                return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

            user = serializer.save()

            return Response({"message": "You have successfully registered"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(VersionedAPIView, APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response = Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            response['Access-Token'] = access_token
            response['Refresh-Token'] = str(refresh)
            return response
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(VersionedAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsOwner)
    lookup_field = 'user__username'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Profile deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class VoteCreateView(VersionedAPIView, generics.CreateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsOwner)
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def perform_create(self, serializer):
        employee = Employee.objects.get(user=self.request.user)

        today = timezone.now().date()
        existing_vote_today = Vote.objects.filter(employee=employee, timestamp__date=today).exists()
        if existing_vote_today:
            raise serializers.ValidationError("You have already voted today. You can only vote once per day.")

        serializer.save(employee=employee)
