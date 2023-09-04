
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from titles.models import Category, Genre, Title
from .filters import TitleFilter
from .mixins import ListCreateDestroyMixin
from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleCreateSerializer, TitleSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('reviews__score')
    )
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly,]
    filter_backends = [DjangoFilterBackend,]
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitleCreateSerializer


class CategoryViewSet(ListCreateDestroyMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ListCreateDestroyMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from titles.models import Review, Title
from .permissions import AuthorOrReadOnly, IsModeratorOrAdmin
from .serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrReadOnly, IsModeratorOrAdmin,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_pk'))
        return title.reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=Title.objects.get(id=self.kwargs.get('title_pk'))
        )


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly, IsModeratorOrAdmin,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_pk'))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=Review.objects.get(id=self.kwargs.get('review_pk'))
        )
