from rest_framework import serializers
from .models import Place, PlaceVideo, PlaceImage


class ImageSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = PlaceImage
        fields = ('image',)


class VideoSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = PlaceVideo
        fields = ('video',)


class PlaceSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    images = ImageSerializer(many=True)
    videos = VideoSerializer(many=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Place
        fields = (
            'id', 'url', 'name', 'description', 'location', 'images', 'videos', 'cover_img'
        )

    def create(self, validated_data):
        imgs = validated_data.pop('images')
        vids = validated_data.pop('videos')
        place = Place.objects.create(**validated_data)
        for img in imgs:
            PlaceImage.objects.create(place=place, **img)
        for vid in vids:
            PlaceVideo.objects.create(place=place, **vid)
        return place
