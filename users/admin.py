from django.contrib import admin

from users.models import User


@admin.register(User)
class UsersAdmin(admin.ModelAdmin):
    """Админка модели User"""
    list_display = ('pk', 'referral_code', 'phone', 'verify_code', 'invited_by')
