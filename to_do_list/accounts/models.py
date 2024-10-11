from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from . import managers

class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True, verbose_name=_("Username"))
    email = models.EmailField(max_length=200, unique=True, verbose_name=_("Email"))
    is_admin = models.BooleanField(default=False, verbose_name=_("Is Admin"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Is Staff"))
    is_active = models.BooleanField(default=True, verbose_name=_("Is Active"))
    is_superuser = models.BooleanField(default=False, verbose_name=_("Is Superuser"))
    update_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    expire_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Expire At"))

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = managers.UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
