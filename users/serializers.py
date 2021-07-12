from django.contrib import auth
from rest_framework import serializers

from .models import User, Student, Teacher


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'profile_image', 'first_name', 'last_name', 'email', 'password', 'is_teacher')
        extra_kwargs = {'password': {'write_only': True}}


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'profile_image', 'first_name', 'last_name', 'email')


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'profile_image', 'first_name', 'last_name', 'grade', 'user']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'profile_image', 'first_name', 'last_name', 'expertise', 'rating', 'user']


class LoginSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
