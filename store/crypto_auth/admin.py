from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserWithCryptoKey
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

admin.site.unregister(User)
admin.site.register(UserWithCryptoKey)