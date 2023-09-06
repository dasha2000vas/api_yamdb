from django.contrib.auth import get_user_model
from rest_framework import filters, mixins, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth.validators import UnicodeUsernameValidator

from users.validators import value_validator
from .permissions import IsAdminOrReadOnly

User = get_user_model()


class CreateOnlyModelViewSet(mixins.CreateModelMixin,
                             GenericViewSet):
    """Creation only mixin"""


class ListCreateDestroyMixin(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'


USERNAME_REGEX = UnicodeUsernameValidator.regex


class UserBaseSerializer(serializers.ModelSerializer):
    """General serializer for all types of users"""
    username = serializers.RegexField(
        regex=USERNAME_REGEX,
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
