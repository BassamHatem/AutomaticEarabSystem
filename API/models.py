from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from users.models import Student, Teacher


class Sentence(models.Model):
    raw = models.CharField(max_length=400)
    diacritized = models.CharField(max_length=400, null=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_diacritized = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    diacritizer = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.raw
