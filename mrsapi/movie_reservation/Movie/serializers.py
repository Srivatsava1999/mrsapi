from rest_framework import serializers
from Movie.models import MovieDirectory

class MovieDirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model=MovieDirectory
        feilds=['__all__']