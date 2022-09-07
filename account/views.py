from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
# from .helpers import send_confirmation_email
from .tasks import send_conf_emails
from rest_framework.generics import ListAPIView, GenericAPIView, UpdateAPIView

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_conf_emails(user, user.activation_code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer




class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response({"msg":"You successfully logged out"}, status=status.HTTP_204_NO_CONTENT)

class ActivationView(APIView):
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            code = serializer.validated_data['activation_code']
            user = get_object_or_404(User, activation_code=code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg':'User successfully activated'})


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser, )


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )



class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)


    def update(self, request, *args, **kwargs):
        object = request.user
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not object.check_password(request.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            object.set_password(request.data.get("new_password"))
            object.is_active = True
            object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    serializer_class = PasswordResetEmailSerializer
    def post(self, request):
        data = request.data
        # email = request.email
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            pass
        return Response('OK', 200)

    @action(['GET'],detail='fe')
    def hello(self):
        return Response("World")