from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6,
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


class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        try:
            email = attrs['data'].get('email', )
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(user.id)
                token = PasswordResetTokenGenerator().make_token(user)
                context = {
                    "email_text_detail": """
                                        Thanks for creating account.
                                        Please verify your account
                                            """,
                    "email": user.email,
                    "activation_code": user.activation_code
                }

                msg_html = render_to_string("email.html", context)
                plain_message = strip_tags(msg_html)
                subject = "Account activation"
                to_emails = user.email
                mail.send_mail(
                    subject,
                    plain_message,
                    "maviboncuaika@gmail.com",
                    [to_emails],
                    html_message=msg_html
                )
            return attrs
        except:
            pass


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True,
                                         min_length=6, write_only=True)
