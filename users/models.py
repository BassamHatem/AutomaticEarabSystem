from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util


# Create your models here.
class MyUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_verified', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(null=False, unique=True, max_length=255)
    is_teacher = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    profile_image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}


'''
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
'''


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="User", on_delete=models.CASCADE,
                                related_name='student', null=False)
    full_name = models.CharField(max_length=50)
    profile_image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    grade = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.full_name


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="User", on_delete=models.CASCADE,
                                related_name='teacher', null=False)
    full_name = models.CharField(max_length=50)
    profile_image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    expertise = models.CharField(max_length=200, null=True)
    rating = models.DecimalField(max_digits=5, decimal_places=3, default=0)

    def __str__(self):
        return self.full_name


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_message = "{}?token={}".format('http://127.0.0.1:8000'+reverse('password-reset:reset-password-request'), reset_password_token.key)
    email_data = {'email_subject': "Password Reset for {title}".format(title="aes.com"), 'email_body': email_message,
                      'to_email': [reset_password_token.user.email]}
    Util.send_email(email_data)
    '''
    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_message,
        # from:
        "noreply@aes.com",
        # to:
        [reset_password_token.user.email]
    )
    '''
