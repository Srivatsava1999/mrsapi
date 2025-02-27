from rest_framework import serializers
from Users.models import UserAccount

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserAccount
        fields='__all__'

class AuthSerializer(serializers.Serializer):
    code=serializers.CharField(required=False)
    error=serializers.CharField(required=False)