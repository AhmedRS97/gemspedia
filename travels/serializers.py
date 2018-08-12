from rest_framework import serializers
from .models import Travel, TravelImage, TravelVideo
from accounts.models import User

# from django.conf import settings


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = TravelImage
        fields = ('image',)


class VideoSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = TravelVideo
        fields = ('video',)


class TravelUserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="accounts:user-detail")

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'biography', 'avatar',)


class TravelSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    url = serializers.HyperlinkedIdentityField(view_name="travels:travel-detail")
    users = TravelUserSerializer(many=True, read_only=True)
    images = ImageSerializer(many=True)
    videos = VideoSerializer(many=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Travel
        fields = (
            'url', 'id', 'title', 'description', 'price', 'has_offer', 'offer', 'start', 'end',
            'limit', 'users', 'duration', 'price_in_cents', 'images', 'videos', 'api_key',
        )
        read_only_fields = ('duration', 'price_in_cents', 'api_key')

    def create(self, validated_data):
        imgs = validated_data.pop('images')
        vids = validated_data.pop('videos')
        validated_data.pop('users')
        validated_data['available_seats'] = validated_data['limit']
        travel = Travel.objects.create(**validated_data)
        for img in imgs:
            TravelImage.objects.create(travel=travel, **img)
        for vid in vids:
            TravelVideo.objects.create(travel=travel, **vid)
        return travel
