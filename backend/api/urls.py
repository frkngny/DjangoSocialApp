from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('users', UserView.as_view()),
    path('profile-create', ProfileCreateView.as_view()),
    path('profiles', ProfileView.as_view()),
    path('profile/<int:pk>', ProfileCreateView.as_view()),
    path('register', RegisterView.as_view(), name='register'),
    path('token', UserTokenObtainView.as_view(), name='user_token_obtain'),
    path('token-refresh', TokenRefreshView.as_view(), name='user_token_refresh'),
    path('user-activity', UserActivityView.as_view()), # user-activity?user_id=1 can be used to get a user's activity
    path('user-activity/update', UserActivityUpdateView.as_view()), # user-activity?user_id=1 will be used to update a user
    path('search-user', UserSearchView.as_view()),

    # Room
    path('rooms', RoomView.as_view()),
    path('create-room', CreateRoomView.as_view()),
    path('join-room', JoinRoomView.as_view()), #?code
    path('room-messages', RoomChatView.as_view(), name='room_chat'), # ?room_code
    path('send-room-message', SendRoomMessageView.as_view(), name='send_room_message'), 
]
