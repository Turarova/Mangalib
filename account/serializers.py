from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

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


class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        fields = ['email']

    def validate(self, attrs):
        try:
            email = attrs.get('email', )
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(user.id)
                token = PasswordResetTokenGenerator().make_token(user)

            return attrs
        except:
            pass