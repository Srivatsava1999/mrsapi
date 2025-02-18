from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email Must Be Sent"))
        email=self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        user=self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', UserAccount.CUSTOMER)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_enterprise_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', UserAccount.ENTERPRISE)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('role', UserAccount.ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)

# Create your models here.

class UserAccount(AbstractBaseUser, PermissionsMixin):
    ADMIN=1
    ENTERPRISE=2
    CUSTOMER=3

    ROLE_CHOICES=(
        (ADMIN, 'Admin'),
        (ENTERPRISE, 'Enterprise'),
        (CUSTOMER, 'Customer'),
    )
    role=models.PositiveSmallIntegerField(choices=ROLE_CHOICES, default=CUSTOMER)
    email=models.EmailField(blank=False, unique=True)
    name=models.CharField(max_length=255, blank=True, default='')
    phone=models.CharField(max_length=15, default='', blank=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    date_joined=models.DateTimeField(default=timezone.now)
    last_login=models.DateTimeField(blank=True, null=True)
    objects=CustomUserManager()
    USERNAME_FIELD="email"
    EMAIL_FIELD="email"
    REQUIRED_FIELDS=[]

    class Meta:
        verbose_name="User"
        verbose_name_plural="Users"
    
    def get_full_name(self):
        return self.name
        
    def get_short_name(self):
        return self.name or self.email.split('@')[0]
