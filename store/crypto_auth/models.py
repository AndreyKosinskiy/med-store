from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.

class UserWithCryptoKey(AbstractBaseUser):
    email = models.EmailField(max_length=254, blank=False, null=False)
    username = models.EmailField(max_length=254, blank=False, null=False)
    password_for_public_key = models.CharField(max_length=254)
    public_key = models.FileField(upload_to="auth/user")
    private_key = models.FileField(upload_to="auth/user")
