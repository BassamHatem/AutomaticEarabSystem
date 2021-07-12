from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Sentence


# Register your models here.
@admin.register(Sentence)
class SentenceModel(admin.ModelAdmin):
    list_filter = ('raw', 'diacritized', 'date_posted')
    list_display = ('raw', 'diacritized', 'date_posted')



