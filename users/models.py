from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
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

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class StudentManager(BaseUserManager):
 
    def create_student(self, full_name, email, grade, password=None):
        if email is None:
            raise TypeError('Users must have an email address.')
        student = Student(full_name=full_name, 
                          email=self.normalize_email(email),
                          grade=grade)
        student.set_password(password)
        student.save()
        return student
 
 
class TeacherManager(BaseUserManager):
 
    def create_teacher(self, full_name, email, expertise, password=None):
        if email is None:
            raise TypeError('Users must have an email address.')
        teacher = Teacher(full_name=full_name, 
                            email=self.normalize_email(email),
                            expertise=expertise)
        teacher.is_teacher=True
        teacher.set_password(password)
        teacher.save()
        return teacher


class User(AbstractUser):
    full_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=False, unique=True, max_length=255)
    profile_image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    is_teacher = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = MyUserManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}


class Student(User):
    GRADE_CHOICES = ((1, 'Primary School'), (2, 'Preparatory School'), (3, 'Secondary School'))
    grade = models.PositiveSmallIntegerField(choices=GRADE_CHOICES, default=2)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'grade']

    objects = StudentManager()

    class Meta:
        verbose_name_plural = 'Students'
    
    def __str__(self):
        return self.full_name


class Teacher(User):
    EXP_CHOICES = ((1, 'Fresh Graduate'), (2, '1-5 Years Experience'), (3, '5+ Years Experience'))
    expertise = models.PositiveSmallIntegerField(choices=EXP_CHOICES, default=2)
    rating = models.DecimalField(max_digits=5, decimal_places=3, default=3.0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'expertise']

    objects = TeacherManager()

    class Meta:
        verbose_name_plural = 'Teachers'
    
    def __str__(self):
        return self.full_name


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_message = "{}?token={}".format('http://127.0.0.1:8000'+reverse('password-reset:reset-password-request'), reset_password_token.key)
    email_data = {'email_subject': "Password Reset for {title}".format(title="aes.com"), 'email_body': email_message,
                      'to_email': [reset_password_token.user.email]}
    Util.send_email(email_data)

