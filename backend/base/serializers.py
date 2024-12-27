from rest_framework import serializers
from .models import Note
from django.contrib.auth.models import User

# Serializer for user registration
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Password should not be returned in responses

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])  # Hash the password before saving
        user.save()
        return user

# Serializer to return basic user info (username only)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

# Serializer for notes (for displaying and creating notes)
class NoteSearilizer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'description']
