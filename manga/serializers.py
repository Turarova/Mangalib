from rest_framework import serializers
from .models import *


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class NovellaSerializer(serializers.ModelSerializer):
    model = Novella
    fields = '__all__'
