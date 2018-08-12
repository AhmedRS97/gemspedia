from rest_framework import serializers
from .models import User

from django.conf import settings
from djoser.compat import get_user_email, get_user_email_field_name
# from djoser.serializers import UserSerializer as DjoserUserSerializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User._meta.pk.name, User.USERNAME_FIELD, 'first_name', 'last_name', 'biography', 'avatar', 'url'
        )
        read_only_fields = (User.USERNAME_FIELD,)

    def update(self, instance, validated_data):
        email_field = get_user_email_field_name(User)
        if settings.SEND_ACTIVATION_EMAIL and email_field in validated_data:
            instance_email = get_user_email(instance)
            if instance_email != validated_data[email_field]:
                instance.is_active = False
                instance.save(update_fields=['is_active'])
        return super(UserSerializer, self).update(instance, validated_data)
