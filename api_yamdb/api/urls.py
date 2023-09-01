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
    'auth/token',
    views.VerifyUserViewSet,
    basename='verify_token',
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
