from rest_framework import serializers
from .models import Sentence


class NewSentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = ['id', 'raw', 'author']


class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        fields = ['id', 'raw', 'diacritized', 'date_posted', 'author', 'diacritizer']
