from django.urls import path
from users.apps import UsersConfig
from users.views import LoginAPIView, ValidateAPIView, UserRetrieveAPIView, UserUpdateAPIView, LogoutAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login_user'),
    path('validate/', ValidateAPIView.as_view(), name='validate_code'),
    path('logout/', LogoutAPIView.as_view(), name='logout_user'),
    path('profile/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_profile'),
    path('profile/update/<int:pk>/', UserUpdateAPIView.as_view(), name='profile_update'),
]
