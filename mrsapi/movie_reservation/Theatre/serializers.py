from rest_framework import serializers
from Theatre.models import TheatreDirectory

class TheatreDirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model=TheatreDirectory
        feilds=['__all__']