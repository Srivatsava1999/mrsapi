from rest_framework import serializers
from Movie.models import MovieDirectory

class MovieDirectorySerializer(serializers.ModelSerializer):
    class Meta:
        model=MovieDirectory
        fields='__all__'