from rest_framework import serializers
from accounts.models import User
from places.models import Place
from .models import Event, EventImage, EventVideo

# from django.conf import settings


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


class EventUserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="accounts:user-detail")

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'biography', 'avatar',)


class EventPlaceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="places:place-detail")

    class Meta:
        model = Place
        fields = ('url', 'id', 'name', 'address')


class EventSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    url = serializers.HyperlinkedIdentityField(view_name="events:event-detail")
    users = EventUserSerializer(many=True)
    # location = EventPlaceSerializer(many=False)
    images = ImageSerializer(many=True)
    videos = VideoSerializer(many=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Event
        fields = (
            'url', 'id', 'title', 'description', 'price', 'start', 'end', 'limit', 'available_seats', 'cover_img',
            'location', 'duration', 'api_key', 'price_in_cents', 'users', 'images', 'videos', 'created',
        )
        read_only_fields = ('duration', 'price_in_cents', 'api_key')

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
