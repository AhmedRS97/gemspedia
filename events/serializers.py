from rest_framework import serializers
from accounts.serializers import UserSerializer
from accounts.models import User
from .models import Event, EventImage, EventVideo

from django.conf import settings


class ImageSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = EventImage
        fields = ('image',)


class VideoSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = EventVideo
        fields = ('video',)


class EventSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    users = UserSerializer(many=True)  # PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    images = ImageSerializer(many=True)
    videos = VideoSerializer(many=True)
    api_key = serializers.Field(source=settings.STRIPE_PUBLIC_KEY)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Event
        fields = (
            'id', 'url', 'title', 'description', 'price', 'start', 'end', 'limit', 'available_seats',
            'location', 'duration', 'api_key', 'price_in_cents', 'users', 'images', 'videos', 'created',
        )
        read_only_fields = ('id', 'duration', 'price_in_cents', 'api_key')

    def create(self, validated_data):
        imgs = validated_data.pop('images')
        vids = validated_data.pop('videos')
        validated_data.pop('users')
        validated_data['available_seats'] = validated_data['limit']
        event = Event.objects.create(**validated_data)
        for img in imgs:
            EventImage.objects.create(event=event, **img)
        for vid in vids:
            EventVideo.objects.create(event=event, **vid)
        return event
