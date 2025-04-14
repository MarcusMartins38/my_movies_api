from django.urls import path
from users.views import RegisterView, UserMeView, PasswordResetRequestView, PasswordResetValidateTokenView, PasswordResetConfirmView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', UserMeView.as_view(), name='me'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset/validate/', PasswordResetValidateTokenView.as_view(), name='password-reset-validate'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]