from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(UserActivity)
admin.site.register(UserRelationship)
admin.site.register(Room)
admin.site.register(RoomChatMessage)