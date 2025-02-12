from rest_framework import serializers
from Booking.models import C_ShowType, ShowDirectory, BookingDirectory
from Theatre.models import TheatreDirectory, ScreenDirectory, SeatMaster
from Movie.models import MovieDirectory

class C_ShowTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=C_ShowType
        fields='__all__'

class ShowDirectorySerializer(serializers.ModelSerializer):
    movieId=serializers.PrimaryKeyRelatedField(queryset=MovieDirectory.objects.all())
    screenId=serializers.PrimaryKeyRelatedField(queryset=ScreenDirectory.objects.all())
    theatreId=serializers.PrimaryKeyRelatedField(queryset=TheatreDirectory.objects.all())
    showTypeId=serializers.PrimaryKeyRelatedField(queryset=ShowDirectory.objects.all())
    class Meta:
        model=ShowDirectory
        fields='__all__'

class BookingDirectorySerializer(serializers.ModelSerializer):
    showId=serializers.PrimaryKeyRelatedField(queryset=ShowDirectory.objects.all())
    seatId=serializers.PrimaryKeyRelatedField(queryset=SeatMaster.objects.all())
    class Meta:
        model=BookingDirectory
        fields='__all__'