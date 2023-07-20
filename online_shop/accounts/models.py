from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

# Custom user model
class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(max_length=255, unique=True)
	phone_number = models.CharField(max_length=11, unique=True)
	full_name = models.CharField(max_length=100)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'phone_number'
	REQUIRED_FIELDS = ['email', 'full_name']

	def __str__(self):
		return self.email

	@property
	def is_staff(self):
		return self.is_admin



# Model class to store the OTP code sent to the user
class OtpCode(models.Model):
	phone_number = models.CharField(max_length=11, unique=True)
	code = models.PositiveSmallIntegerField()
	created = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.phone_number} - {self.code} - {self.created}'
	


# Model class to represent the user's address
class Address(models.Model):
	country = models.CharField(max_length=100)
	province = models.CharField(max_length=100)
	city = models.CharField(max_length=100)
	street = models.CharField(max_length=100)
	plaque = models.IntegerField()
	postal_code = models.IntegerField()
	
	def get_address(self):
		return f'{self.street}, {self.plaque}, {self.city}, {self.province}, {self.country}'
	# Function to return the complete user address
	