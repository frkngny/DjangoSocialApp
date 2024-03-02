from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileCreateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

class ProfileView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class UserTokenObtainView(TokenObtainPairView):
    serializer_class = UserTokenObtainSerializer

class UserActivityView(APIView):
    serializer_class = UserActivitySerializer
    lookup_kwarg = 'user_id'
    
    def get(self, request):
        if request.GET.get(self.lookup_kwarg):
            queryset = UserActivity.objects.get(user=request.GET.get(self.lookup_kwarg))
            if queryset.exists():
                data = UserActivitySerializer(queryset[0]).data
                return Response(data)
        return Response(UserActivitySerializer(UserActivity.objects.all(), many=True).data)
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_id = serializer.data.get('user')
            user_status = serializer.data.get('status')
            listening_to = serializer.data.get('listening_to')
            queryset = UserActivity.objects.get(user=user_id)
            if not queryset.exists():
                user = User.objects.get(id=user_id)
                if user.exists():
                    user = user[0]
                    user_activity = UserActivity(user=user, status=user_status, listening_to=listening_to)
                    user_activity.save()
                    return Response(UserActivitySerializer(user_activity).data, status=status.HTTP_201_CREATED)
                return Response({"Bad Request": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"Bad request": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)


class UserActivityUpdateView(APIView):
    serializer_class = UpdateUserActivitySerializer
    lookup_kwarg = 'user_id'

    def get(self, request):
        if request.GET.get(self.lookup_kwarg):
            queryset = UserActivity.objects.get(user=request.GET.get(self.lookup_kwarg))
            if queryset.exists():
                data = UserActivitySerializer(queryset[0]).data
                return Response(data)
            else:
                return Response({"Bad Request": f"User with given '{self.lookup_kwarg}' is not found."}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserActivitySerializer(UserActivity.objects.all(), many=True).data)

    
    def put(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            if request.query_params.get(self.lookup_kwarg):
                user = request.query_params.get(self.lookup_kwarg)
                user_status = serializer.data.get('status')
                listening_to = serializer.data.get('listening_to')
                queryset = UserActivity.objects.get(user=user)
                if queryset.exists():
                    user_activity = queryset[0]
                    user_activity.status = user_status
                    user_activity.listening_to = listening_to
                    user_activity.save(update_fields=['status', 'listening_to'])
                    return Response(UserActivitySerializer(user_activity).data, status=status.HTTP_200_OK)
                else:
                    return Response({"Bad Request": f"User with given '{self.lookup_kwarg}' is not found."}, status=status.HTTP_404_NOT_FOUND)
            return Response({"Bad request": f"'{self.lookup_kwarg}' is not given as parameter."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Bad request": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)

class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class CreateRoomView(APIView):
    serializer_class = RoomSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            user = serializer.data.get('user')
            room = Room(name=name, creator=user)
            room.save()
            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
        return Response({'Bad request': 'Invalid data.', 'error': serializer.errors()}, status=status.HTTP_400_BAD_REQUEST)

class JoinRoomView(APIView):
    serializer_class = RoomSerializer

    def post(self, request):
        code = request.data.get('code')
        if code:
            queryset = Room.objects.filter(code=code)
            if queryset.exists():
                room = queryset[0]
                return Response({'Message': 'Joined to room.'}, status=status.HTTP_200_OK)
            return Response({'Bad request': 'Room does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad request': 'Please enter a valid code.'}, status=status.HTTP_404_NOT_FOUND)