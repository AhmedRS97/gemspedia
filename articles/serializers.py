from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Article, ArticleVideo


class VideoSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = ArticleVideo
        fields = ('video',)


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    user = UserSerializer(read_only=True)
    videos = VideoSerializer(many=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Article
        fields = (
            'id', 'url', 'title', 'description', 'slug', 'cover_img', 'user', 'videos', 'created', 'updated',
        )
        read_only_fields = ('id', 'created',)

    def create(self, validated_data):
        vids = validated_data.pop('videos')
        article = Article.objects.create(**validated_data)
        for vid in vids:
            ArticleVideo.objects.create(article=article, **vid)
        return article
