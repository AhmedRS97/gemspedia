# from rest_framework import serializers
from .models import User
from djoser.serializers import UserSerializer as DjoserUserSerializer


class UserSerializer(DjoserUserSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = User
        fields = DjoserUserSerializer.Meta.fields + ('first_name', 'last_name', 'biography', 'avatar')
