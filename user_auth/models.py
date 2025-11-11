from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email field cannot be empty")

        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)

        user = self.model(email=email, **extra_fields)

        if not password:
            password = self.make_random_password(length=12)

        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValidationError("Superuser must have is_staff=True")
        if not extra_fields.get('is_superuser'):
            raise ValidationError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=256, unique=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    password = models.CharField(max_length=128, validators=[MinLengthValidator(12)])
    role = models.CharField(default="user")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_registered = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

        if User.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError({'email': 'Email already linked to an existing account'})

    def clean_phone_number(self):
        if not self.phone_number:
            return

        n = len(self.phone_number)
        ke_country_code = '254'

        if n not in [10, 12]:
            raise ValidationError({'phone_number': 'Phone number must be 10 or 12 digits long'})

        if n == 10 and self.phone_number.startswith('0'):
            self.phone_number = ke_country_code + self.phone_number[1:]

        elif n == 12 and not self.phone_number.startswith(ke_country_code):
            raise ValidationError({'phone_number': 'Invalid country code format'})

        return self.phone_number

    def __str__(self):
        return self.email
