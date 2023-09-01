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
