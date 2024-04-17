from rest_framework import serializers
from user.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'password', 'email']

class TokensSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()

class RefreshTokenSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['refresh_token']

class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()

class RetrieveDataSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']

class ChangeDataSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['username']

