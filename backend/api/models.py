from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
import random
import string

STATUS_CHOICES = {
    "online": "Online",
    "away": "Away",
    "offline": "Offline"
}

RELATION_CHOICES = {
    "sent": "sent",
    "accepted": "accepted"
}

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def __str__(self) -> str:
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=300, null=True, blank=True)
    image = models.ImageField(default="default.jpg", upload_to="user_images", null=True, blank=True)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)

    def get_friends(self):
        return self.friends.all()
    
    def get_friends_count(self):
        return self.friends.all().count()

    def __str__(self) -> str:
        return self.full_name
    
    def save(self, *args, **kwargs):
        if self.full_name == "" or not self.full_name:
            self.full_name = self.user.username
        super(Profile, self).save(*args, **kwargs)

class UserActivity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="online")
    listening_to = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.user} - {self.status} - {self.listening_to}"

class UserRelationship(models.Model):
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=RELATION_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.sender} - {self.receiver} - {self.status}"


def unique_code_generator():
    length = 10
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if not Room.objects.filter(code=code).exists():
            break
    return code


class Room(models.Model):
    code = models.CharField(max_length=10, default=unique_code_generator, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class RoomChatMessage(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='room')
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='sender')
    message = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']
        verbose_name_plural = 'RoomChatMessage'
    
    def __str__(self) -> str:
        return f"{self.room.code} - {self.sender} - {self.date}"

    def get_room(self):
        room_ = Room.objects.get(code=self.room.code)
        return room_
    
    def get_sender(self):
        sender_ = Profile.objects.get(user=self.sender)
        return sender_