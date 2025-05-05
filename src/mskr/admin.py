from django.contrib import admin
from django.contrib.auth.models import User

from .models import Profile
from chat.models import *


class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    #Display username and email fields on admin page
    fields = ["username", "email", "last_name", "first_name"]
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Chat)

