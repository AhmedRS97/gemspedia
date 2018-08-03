from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Travel, TravelImage, TravelVideo


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


class TravelSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    users = UserSerializer(many=True)
    images = ImageSerializer(many=True)
    videos = VideoSerializer(many=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Travel
        fields = (
            'users', 'title', 'description', 'price', 'has_offer', 'offer', 'start', 'end',
            'limit', 'location', 'images', 'videos',
        )
        read_only_fields = ('duration',)

    def create(self, validated_data):
        imgs = validated_data.pop('images')
        vids = validated_data.pop('videos')
        travel = Travel.objects.create(**validated_data)
        for img in imgs:
            TravelImage.objects.create(travel=travel, **img)
        for vid in vids:
            TravelVideo.objects.create(travel=travel, **vid)
        return travel
