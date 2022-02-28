import email
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Account(AbstractBaseUser):
    email           = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username        = models.CharField(max_length=30, unique=True)
    date_joined     = models.DateTimeField(verbose_name="date joined", auto_now_true=True)
    last_login      = models.DateTimeField(verbose_name="date joined", auto_now=True)
    is_admin        = models.BooleanField(default=False)
    is_active       = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_superuser    = models.BooleanField(default=False)
    profile_image   = models.ImageField(max_Length=255, upLoad_to=, null=True, blank=True, default=)