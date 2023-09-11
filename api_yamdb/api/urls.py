from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

v1_router = DefaultRouter()

auth_urls = [
    path('signup/', views.SignUpViewSet.as_view({'post': 'create'}), name='signup'),
    path('token/', views.VerifyViewSet.as_view({'post': 'create'}), name='token'),
]

v1_router.register('users', views.UserViewSet)
v1_router.register('titles', views.TitleViewSet, basename='titles')
v1_router.register('categories', views.CategoryViewSet, basename='categories')
v1_router.register('genres', views.GenreViewSet, basename='genres')
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews',
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/', include(auth_urls))
]
