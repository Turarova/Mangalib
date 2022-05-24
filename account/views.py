from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from .helpers import send_confirmation_email
from rest_framework.generics import ListAPIView, GenericAPIView, UpdateAPIView

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_confirmation_email(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated, ]
#
#     def post(self, request):
#         user = request.user
#         Token.objects.filter(user=user).delete()
#         return Response('Successfully logged out', status=status.HTTP_200_OK)




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


class PasswordResetEmailView(GenericAPIView):
    serializer_class = PasswordResetEmailSerializer
    def post(self, request):
        data = {'request':request, 'data':request.data}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)



class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)