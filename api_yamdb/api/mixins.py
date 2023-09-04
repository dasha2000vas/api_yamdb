from rest_framework import filters, mixins, viewsets

from .permissions import IsAdminOrReadOnly


class ListCreateDestroyMixin(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [IsAdminOrReadOnly,]
    filter_backends = [filters.SearchFilter,]
    search_fields = ('name',)
    lookup_field = 'slug'
