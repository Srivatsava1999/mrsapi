from rest_framework import serializers
from Users.models import UserAccount

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserAccount
        fields='__all__'