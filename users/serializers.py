from rest_framework import serializers
from users.models import User


class UserLoginSerializer(serializers.ModelSerializer):
    """Сериализатор входа/регистрации пользователя"""
    class Meta:
        model = User
        fields = ('phone',)


class UserValidateSerializer(serializers.ModelSerializer):
    """Сериализатор проверки кода верификации"""
    class Meta:
        model = User
        fields = ('phone', 'verify_code')


class UserProfileSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля пользователя"""
    invited_users = serializers.SerializerMethodField()

    def get_invited_users(self, obj):
        """Возвращает список приглашенных пользователей"""
        return obj.user_set.all().values_list('phone', flat=True)

    class Meta:
        model = User
        fields = ('id', 'phone', 'referral_code', 'invited_code', 'invited_users')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для редактирования профиля пользователя"""

    class Meta:
        model = User
        fields = ('invited_code', 'avatar',)

