from rest_framework.routers import DefaultRouter
from django.urls import include, path

from . import views

v1_router = DefaultRouter()

v1_router.register('users', views.UserViewSet, basename='users')
v1_router.register('users/me', views.MySelfUserViewSet, basename='my_user')
v1_router.register(
    'auth/signup',
    views.SignUpUserViewSet,
    basename='signup',
)
v1_router.register(
    r'titles/(?P<title_pk>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_pk>\d+)/reviews/(?P<review_pk>\d+)/comments',
    views.CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
