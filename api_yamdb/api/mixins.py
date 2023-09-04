from django.contrib.auth import get_user_model
from rest_framework import mixins, serializers
from rest_framework.viewsets import GenericViewSet

from users.validators import value_validator

User = get_user_model()


class CreateOnlyModelViewSet(mixins.CreateModelMixin,
                             GenericViewSet):
    """Creation only mixin"""


class UserBaseSerializer(serializers.ModelSerializer):
    """General serializer for all types of users"""
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        max_length=150,
        required=True,
        validators=[value_validator],
    )
    email = serializers.EmailField(
        max_length=254,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
