from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class CreateOnlyModelViewSet(mixins.CreateModelMixin,
                             GenericViewSet):
    """Creation user mixin"""
    ...
