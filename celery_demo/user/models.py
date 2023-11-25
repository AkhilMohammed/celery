from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

def five_min_from_now():
    return timezone.now()+timezone.timedelta(minutes=5)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('the email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user 

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('super user must have is_staff = True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('super user must have is_superuser=True')

        return self.create_user(email, password, **extra_fileds)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    userName = models.CharField(max_length=30, unique=True, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    date_joined =  models.DateTimeField(default=timezone.now)
    firstName = models.CharField(max_length=30)
    lastName = models.CharField(max_length=30)
    otp = models.IntegerField()
    userType = models.CharField(max_length=30)
    profilePicture = models.URLField(null =True,blank=True)
    LastLogin = models.DateTimeField(null=True,blank=True)
    expiry_time = models.DateTimeField(default = five_min_from_now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def _str_(self):
        return self.email


class UserToken(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token_id = models.CharField(unique=True)
    created_time = models.DateTimeField(default= timezone.now)
    is_active = models.BooleanField(default=True)

class BlacklistedToken(models.Model):
    token_id = models.ForeignKey(UserToken, on_delete=models.CASCADE)
    date = models.DateTimeField(default = timezone.now)