from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Article, ArticleVideo
from accounts.models import User


class VideoSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = ArticleVideo
        fields = ('video',)


class ArticleUserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="accounts:user-detail")

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'first_name', 'last_name', 'biography', 'avatar',)


class ArticleSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    url = serializers.HyperlinkedIdentityField(view_name="articles:article-detail")
    user = ArticleUserSerializer(many=False, read_only=True)
    videos = VideoSerializer(many=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Article
        fields = (
            'url', 'id', 'title', 'description', 'slug', 'cover_img', 'user', 'videos', 'created', 'updated',
        )
        read_only_fields = ('created',)

    def create(self, validated_data):
        vids = validated_data.pop('videos')
        article = Article.objects.create(**validated_data)
        for vid in vids:
            ArticleVideo.objects.create(article=article, **vid)
        return article
