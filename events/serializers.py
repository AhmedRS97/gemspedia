from rest_framework import serializers
# from accounts.serializers import UserSerializer
from accounts.models import User
from .models import Event, EventImage, EventVideo


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


class EventSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    images = ImageSerializer(many=True)
    videos = VideoSerializer(many=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Event
        fields = (
            'users', 'title', 'description', 'price', 'start', 'end',
            'limit', 'location', 'images', 'videos',
        )
        read_only_fields = ('duration', 'price_in_cents')

    def create(self, validated_data):
        imgs = validated_data.pop('images')
        vids = validated_data.pop('videos')
        validated_data.pop('users')
        event = Event.objects.create(**validated_data)
        for img in imgs:
            EventImage.objects.create(event=event, **img)
        for vid in vids:
            EventVideo.objects.create(event=event, **vid)
        return event
