from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import IntegrityError
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import UserSerializer, TokenSerializer
from .permissions import IsAdmin
from .mixins import CreateOnlyModelViewSet

User = get_user_model()


@action(
    methods=['get', 'patch'],
    detail=False,
    permission_classes=[IsAuthenticated, IsAdmin],
)
class MySelfUserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.request.user


@action(
    methods=['get', 'post', 'patch', 'delete'],
    detail=True,
    permission_classes=[IsAdmin],
)
class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = LimitOffsetPagination


class SignUpUserViewSet(CreateOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        try:
            user, _ = User.objects.get_or_create(
                **serializer.validated_data,
            )
        except IntegrityError:
            return Response(
                'This login or email is already exists',
                status=status.HTTP_400_BAD_REQUEST
            )
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = str(confirmation_code)
        print(user.confirmation_code)
        user.save()

        send_mail(
            subject='Email Verification Request',
            message=f'Your verification code: {confirmation_code}',
            from_email=settings.AUTH_EMAIL,
            recipient_list=(user.email,),
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save()
