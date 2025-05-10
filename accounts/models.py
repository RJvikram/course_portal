from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext as _
from django.utils.safestring import mark_safe
from django.db import models

class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        """Create and save a User with the given phone number and password."""
        if not phone_number:
            raise ValueError('The given phone number must be set')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password=None, **extra_fields):
        """Create and save a regular User with the given phone number and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        """Create and save a SuperUser with the given phone number and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, password, **extra_fields)

class User(AbstractUser):
    username = None
    phone_number = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    join_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        db_table = 'users'
        indexes = [
            models.Index(fields=['phone_number']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.phone_number} - {self.email}"

class UserBasicDetails(models.Model):
    SEX_CHOICES = (('Female', 'Female'), ('Male', 'Male'), ('Other', 'Other'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='basic_info')
    full_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=SEX_CHOICES)
    profile_image = models.ImageField(upload_to="user_profile", default="user_profile/user.jpeg", blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    aadhaar_number = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        db_table = "user_basic_details"
    
    def image_tag(self):
        if self.profile_image:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.profile_image.url)
        else:
            return 'No Image Found'
    image_tag.short_description = 'Image'

    def save(self, *args, **kwargs):
        if self.user.first_name and self.user.last_name:
            self.full_name = self.user.first_name + self.user.last_name

        super().save(*args, **kwargs)
    
    def __str__(self):
        return str(self.full_name)