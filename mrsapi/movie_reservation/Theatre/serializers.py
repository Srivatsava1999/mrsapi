from rest_framework import serializers
from Theatre.models import TheatreDirectory,ScreenDirectory,SeatMaster

class TheatreDirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model=TheatreDirectory
        fields='__all__'

class ScreenDirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ScreenDirectory
        fields='__all__'
        depth=1

class SeatMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model=SeatMaster
        fields='__all__'
        depth=1