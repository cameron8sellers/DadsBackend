from .models import User
from django.contrib.auth import authenticate
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        max_length=55,
        min_length=8,
        write_only=True
    )
    token = serializers.CharField(max_length=255, read_only=True)
    class Meta:
        model = User

        fields = ('username', 'email', 'first_name','password', 'token')
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):

    email = serializers.CharField(max_length=55, read_only=True)
    username = serializers.CharField(max_length=55)
    password = serializers.CharField(max_length=55, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'token')

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError(
                'Username required to login'
            )
        if password is None:
            raise serializers.ValidationError(
                'Password is required for login'
            )
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A User with that user name was not found'
            )
        if not user.is_active:
            raise serializers.ValidationError(
                'This User has been deactivated'
            )

        return {
            "username": user.username,
            "email": user.email,
            "token": user.token
        }
