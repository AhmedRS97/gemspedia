from rest_framework import serializers
from accounts.models import User
from places.models import Place
from .models import Event, EventImage, EventVideo
# from django.shortcuts import get_object_or_404

# from django.conf import settings


class ImageSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = EventImage
        fields = ('id', 'image',)


class VideoSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = EventVideo
        fields = ('id', 'video',)


class EventUserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="accounts:user-detail")

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'biography', 'avatar',)


class EventPlaceSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="places:place-detail")

    class Meta:
        model = Place
        fields = ('url', 'id', 'name', 'address')


class ReadEventSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    url = serializers.HyperlinkedIdentityField(view_name="events:event-detail")
    users = EventUserSerializer(many=True)
    location = EventPlaceSerializer(many=False)
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
        depth = 1


class WriteEventSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="events:event-detail")
    location = serializers.PrimaryKeyRelatedField(many=False, queryset=Place.objects.all())
    images = ImageSerializer(many=True)
    videos = VideoSerializer(many=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Event
        fields = (
            'id', 'url', 'title', 'description', 'price', 'start', 'end', 'limit', 'available_seats', 'cover_img',
            'location', 'duration', 'api_key', 'price_in_cents', 'users', 'images', 'videos',
        )
        read_only_fields = ('duration', 'price_in_cents', 'api_key')

    def create(self, validated_data):
        validated_data.pop('users', None)  # no users will be associated at the creation of the event.
        validated_data.pop('images', None)  # removing empty images from validated data and use the images in context.
        validated_data.pop('videos', None)  # the same above comment but with videos instead :D
        validated_data['available_seats'] = validated_data['limit']
        event = Event.objects.create(**validated_data)
        for img in self.context.get('images'):
            EventImage.objects.create(event=event, image=img)
        for vid in self.context.get('videos'):
            EventVideo.objects.create(event=event, video=vid)
        return event

    def update(self, instance, validated_data):
        Event.objects.update()
