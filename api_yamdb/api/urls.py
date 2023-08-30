from django.urls import include, path
from rest_framework import routers

from .views import ReviewViewSet, CommentViewSet


v1_router = routers.DefaultRouter()
v1_router.register(
    r'titles/(?P<title_pk>\d+)/reviews', ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_pk>\d+)/reviews/(?P<review_pk>\d+)/comments',
    CommentViewSet, basename='comments'
)

urls = [
    path('v1/', include(v1_router.urls)),
]
