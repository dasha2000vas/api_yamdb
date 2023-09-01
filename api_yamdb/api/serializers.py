from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=256, required=True)
