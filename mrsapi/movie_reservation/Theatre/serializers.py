from rest_framework import serializers
from Theatre.models import TheatreDirectory,ScreenDirectory,SeatMaster

class TheatreDirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model=TheatreDirectory
        fields='__all__'

class ScreenDirectorySerializer(serializers.ModelSerializer):
    theatreId = serializers.PrimaryKeyRelatedField(queryset=TheatreDirectory.objects.all())
    class Meta:
        model=ScreenDirectory
        fields='__all__'

class SeatMasterSerializer(serializers.ModelSerializer):
    screenId=serializers.PrimaryKeyRelatedField(queryset=ScreenDirectory.objects.all())
    class Meta:
        model=SeatMaster
        fields='__all__'