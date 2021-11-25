from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.


# for password encryption support

class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)
