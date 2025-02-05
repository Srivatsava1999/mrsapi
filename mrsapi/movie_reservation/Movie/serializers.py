from rest_framework import serializers

class MovieDirectorySerializers(serializers.ModelSerializer):
    class Meta:
        model=MovieDirectory
        feilds=['__all__']