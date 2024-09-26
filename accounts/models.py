from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.constants import BRANCH_CHOICES, YEAR_CHOICES, CLUB_ADMIN_CHOICES
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone
from datetime import timedelta
from django.core.validators import EmailValidator
from django.urls import reverse


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        rollno = extra_fields.pop("rollno", None)
        branch = extra_fields.pop("branch", None)
        year = extra_fields.pop("year", None)

        if not rollno or not branch or not year:
            raise ValueError("Roll number, branch, and year must be set")

        email = self.normalize_email(email)
        user = self.model(
            email=email, rollno=rollno, branch=branch, year=year, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("name", "Admin")
        extra_fields.setdefault("rollno", 1000000000000)
        extra_fields.setdefault("phoneno", 1000000000)
        extra_fields.setdefault("branch", "ADMIN")
        extra_fields.setdefault("year", "ADMIN")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True, primary_key=True, validators=[EmailValidator()]
    )
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    profile_picture = models.ImageField(
        upload_to="profile_pics/", blank=True, null=True
    )
    rollno = models.IntegerField(
        validators=[MaxValueValidator(9999999999999), MinValueValidator(1000000000000)],
        unique=True,
    )
    branch = models.CharField(choices=BRANCH_CHOICES, max_length=5)
    year = models.CharField(choices=YEAR_CHOICES, max_length=5)
    club_admin = models.CharField(
        choices=CLUB_ADMIN_CHOICES, default="NORMAL", max_length=20
    )
    phoneno = models.IntegerField(
        validators=[MinValueValidator(5000000000), MaxValueValidator(9999999999)],
        unique=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse("student", args=[self.rollno])


# Forget Password OTP Model
class UserOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(minutes=10)


# ----------------NOTIFICATION RELATED MODELS----------------


class NotificationSeenStatus(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} | {self.seen}"


class UserSpecificNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notification = models.CharField(blank=False, max_length=255)
    timeStamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.name} | {self.notification[:20]}..."


class NotificationForAll(models.Model):
    notification = models.CharField(blank=False, max_length=255)
    timeStamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.notification[:25]}..."
