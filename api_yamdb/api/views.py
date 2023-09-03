from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import AccessToken

from titles.models import Review, Title
from .permissions import AuthorOrReadOnly, IsModeratorOrAdmin
from .serializers import (
    UserSerializer,
    UserSignUpSerializer,
    TokenSerializer,
    ReviewSerializer,
    CommentSerializer
)
from .permissions import IsAdmin
from .mixins import CreateOnlyModelViewSet

User = get_user_model()


class SignUpUserViewSet(CreateOnlyModelViewSet):
    serializer_class = UserSignUpSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user, _ = User.objects.get_or_create(
                **serializer.validated_data,
            )
        except IntegrityError:
            return Response(
                'This login or email is already exists',
                status=status.HTTP_400_BAD_REQUEST,
            )

        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()

        user.email_user(
            subject='Email Verification Request',
            message=f'{user.username}, your verification code: {confirmation_code}',
            from_email=settings.AUTH_EMAIL,
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'username'
    lookup_url_kwarg = 'username'
    search_fields = ['username']
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = LimitOffsetPagination
    filter_backends = [SearchFilter]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user, _ = User.objects.get_or_create(
                    **serializer.validated_data,
                )
                user.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED,
                )
            except IntegrityError:
                return Response(
                    'This login or email is already exists',
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return super().create(request)

    @action(
        detail=False,
        methods=['get', 'patch', 'post'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                if 'role' in serializer.validated_data:
                    serializer.validated_data.pop('role')
                serializer.save()
                return Response(
                    serializer.validated_data,
                    status=status.HTTP_200_OK
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyUserViewSet(CreateOnlyModelViewSet):
    serializer_class = TokenSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            user = get_object_or_404(
                User,
                username=serializer.validated_data['username'],
            )
            return user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = serializer.validated_data['confirmation_code']
            user = self.get_queryset()
            if default_token_generator.check_token(user, confirmation_code):
                token = AccessToken.for_user(user)
                return Response(
                    {'token': str(token)},
                    status=status.HTTP_200_OK,
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().create(request)


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
