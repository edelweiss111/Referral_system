from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from users.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from users.permissions import IsOwner
from users.serializers import UserProfileSerializer, UserWithoutCodeSerializer, UserWithCodeSerializer, \
    UserLoginSerializer, UserValidateSerializer
from users.services import generate_code, send_otp
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer


class LogoutAPIView(APIView):
    """Вьюсет для выхода из текущего пользователя"""

    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    """Вьюсет входа/регистрации пользователя"""

    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(self, request):
        phone = str(request.data.get('phone', ''))

        # Валидация на коректность номера телефона
        if len(phone) < 10 or len(phone) > 10 or phone.isdigit() is False:
            return Response({'message': 'Номер телефона должен содержать 10 цифр, начиная с 9'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            user = User.objects.create(
                phone=phone,
            )
            user.save()
        finally:
            verify_code = generate_code()
            user.verify_code = verify_code
            user.save()

            send_otp(verify_code, phone)

            return Response({'message': 'На ваш телефон был отправлен код авторизации'}, status=status.HTTP_200_OK)


class ValidateAPIView(APIView):
    """Вьюсет проверки кода для авторизации"""
    permission_classes = [AllowAny]

    @swagger_auto_schema(request_body=UserValidateSerializer)
    def post(self, request):
        phone = request.data.get('phone', '')
        verify_code = int(request.data.get('verify_code', ''))

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь с таким номером не найден'}, status=status.HTTP_404_NOT_FOUND)

        if user.verify_code == verify_code:
            user.verify_code = None
            user.save()

            token, _ = Token.objects.get_or_create(user=user)

            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Неправильный код'}, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Профиль пользователя"""
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwner]


class UserUpdateAPIView(generics.UpdateAPIView):
    """Редактирования профиля пользователя"""
    queryset = User.objects.all()
    permission_classes = [IsOwner]

    def perform_update(self, serializer):
        """Проверка реферального кода и присваивание пригласивший пользователь"""
        user = serializer.save()
        invited_code = self.request.data['invited_code']

        try:
            inviting_user = User.objects.get(referral_code=invited_code)
        except User.DoesNotExist:
            raise APIException('Неверный код')
        else:
            user.invited_by = inviting_user
            user.invited_code = invited_code
            user.save()

    def get_serializer_class(self):
        """Если пользователь уже ввел инвайт код, выбирается сериализатор без возможности редактирования кода"""
        if self.request.user.invited_code is None:
            return UserWithoutCodeSerializer
        return UserWithCodeSerializer