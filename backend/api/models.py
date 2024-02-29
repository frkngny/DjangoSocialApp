from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


STATUS_CHOICES = {
    "online": "Online",
    "away": "Away",
    "offline": "Offline"
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

    def __str__(self) -> str:
        return self.full_name
    
    def save(self, *args, **kwargs):
        if self.full_name == "" or not self.full_name:
            self.full_name = self.user.username
        super(Profile, self).save(*args, **kwargs)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)


class UserActivity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="offline")
    listening_to = models.CharField(max_length=50, null=True, blank=True)