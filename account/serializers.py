from dataclasses import field
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .tasks import send_pass_res
from .models import PasswordReset
# from .helpers import send_confirmation_email

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8,
                                     required=True,
                                     write_only=True)
    class Meta:
        model = User
        fields = ('email', 'password')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('User with this email already exists')
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(TokenObtainPairSerializer):
    pass

class ActivationSerializer(serializers.Serializer):
    activation_code = serializers.CharField(required=True,
                                            write_only=True,
                                            max_length=255)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError as exc:
            self.fail('bad_token')


class PasswordResetEmailSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField()
    # print("TYPEEE", type(email))

    class Meta:
        model = PasswordReset
        fields = '__all__'

    def validate(self, attrs):
        try:
            email = attrs.get('email')
            if User.objects.filter(email=email).exists():
                print(2)
                user = User.objects.get(email=email)
                print(3)
                token = PasswordResetTokenGenerator().make_token(user)
                print(4)
                send_pass_res.delay(user.email)
                print(5)
            return attrs
        except Exception as e:
            raise ValidationError()


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True,
                                         min_length=8, write_only=True)
