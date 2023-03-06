# from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
# from phonenumber_field.modelfields import PhoneNumberField
# from phonenumbers import format_number, PhoneNumberFormat


# Create your models here.
# class CustomUserManager(BaseUserManager):
#     def create_user(self, phone_number, password=None, **extra_fields):
#         if not phone_number:
#             raise ValueError('The Phone Number field must be set')
#         user = self.model(phone_number=phone_number, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, phone_number, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(phone_number, password, **extra_fields)
#
#     def get_by_natural_key(self, phone_number):
#         return self.get(phone_number=phone_number)

#
# class User(AbstractUser): phone_number = PhoneNumberField(unique=True) is_active = models.BooleanField(
# default=True) is_staff = models.BooleanField(default=False) # groups = models.ManyToManyField( #
# related_name='auth_user_set', #     blank=True, #     help_text='The groups this user belongs to. A user will get
# all permissions granted to each of their groups.') #
#
#     USERNAME_FIELD = 'phone_number'
#     objects = CustomUserManager()
#
#     def __str__(self):
#         return str(self.phone_number.as_e164)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('Phone Number is Required !')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(phone_number, password, **extra_fields)


#
class User(AbstractUser):
    phone_number = models.CharField(max_length=200, blank=True, null=True, unique=True)
    is_phone_verified = models.BooleanField("Is Phone Verified", default=False)
    otp = models.CharField(max_length=10, blank=True, null=True)
    username = None

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = UserManager()

    # def __str__(self):
    #     return format_number(self.phone_number, PhoneNumberFormat.E164)


# class User(AbstractBaseUser, PermissionsMixin):
#     phone_number = PhoneNumberField(unique=True)
#     otp = models.CharField(max_length=6, blank=True, null=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     username = None
#
#     USERNAME_FIELD = 'phone_number'
#     REQUIRED_FIELDS = []
#     objects = UserManager()
#
#     def __str__(self):
#         return format_number(self.phone_number, PhoneNumberFormat.E164)
