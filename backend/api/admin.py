from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class AdminUser(UserAdmin):
    list_display = ['username', 'email']

admin.site.register(User, AdminUser)
admin.site.register(Profile)
admin.site.register(UserActivity)
admin.site.register(UserRelationship)
admin.site.register(Room)
admin.site.register(RoomChatMessage)