from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from core.models import BaseModel
from .managers import UserManager
# kaak


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']

    # groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups', blank=True)
    # user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions', blank=True)

    def __str__(self):
        return self.email
        # return self.phone_number

    @property
    def is_staff(self):
        return self.is_admin
    

class Address(BaseModel):
    address = models.CharField(max_length=200)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.address
    

class OtpCode(BaseModel):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.PositiveSmallIntegerField() #خطای این هندل شود
    create = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.phone_number} - {self.code} - {self.create}'