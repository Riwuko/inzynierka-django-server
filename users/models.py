from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from users.account_manager import AccountManager


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)

    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
