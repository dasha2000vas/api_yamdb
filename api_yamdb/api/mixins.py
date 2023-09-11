from django.contrib.auth import get_user_model
from rest_framework import filters, mixins
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import BasePermission

User = get_user_model()


class CreateOnlyModelMixin(mixins.CreateModelMixin,
                           GenericViewSet):
    """Creation only mixin"""


class ListCreateDestroyMixin(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)
    lookup_field = 'slug'


class AdminPermissionMixin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
