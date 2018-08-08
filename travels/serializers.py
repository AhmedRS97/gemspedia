from rest_framework import serializers
# from accounts.serializers import UserSerializer
from .models import Travel, TravelImage, TravelVideo
from accounts.models import User

from django.conf import settings


class ImageSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = TravelImage
        fields = ('image',)


class VideoSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = TravelVideo
        fields = ('video',)


class TravelSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())
    images = ImageSerializer(many=True)
    videos = VideoSerializer(many=True)
    api_key = serializers.Field(source=settings.STRIPE_PUBLIC_KEY)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Travel
        fields = (
            'id', 'title', 'description', 'price', 'has_offer', 'offer', 'start', 'end', 'limit', 'users',
            'location', 'duration', 'price_in_cents', 'images', 'videos', 'api_key',
            # 'url',
        )
        read_only_fields = ('id', 'duration', 'price_in_cents', 'api_key')

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
