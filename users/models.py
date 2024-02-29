from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Моодель пользователя"""

    username = None

    phone = models.CharField(max_length=10, unique=True, verbose_name='Телефон')
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)
    verify_code = models.PositiveSmallIntegerField(verbose_name='Код верификации', **NULLABLE)
    invited_by = models.ForeignKey('User', on_delete=models.SET_NULL, **NULLABLE, verbose_name='Кем приглашен')
    referral_code = models.CharField(max_length=6, default=get_random_string(6),
                                     verbose_name='Реферальный код пользователя')
    invited_code = models.CharField(max_length=6, **NULLABLE, verbose_name='Код приглашения')

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []
