from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from users.models import User, Student, Teacher


# Register your models here.
@admin.register(Student)
class StudentModel(admin.ModelAdmin):
    list_filter = ('full_name',)
    list_display = ('full_name',)
    search_fields = ('full_name', 'email')


@admin.register(Teacher)
class TeacherModel(admin.ModelAdmin):
    list_filter = ('full_name',)
    list_display = ('full_name',)
    search_fields = ('full_name', 'email')


admin.site.unregister(Group)
