from django.urls import path
from .views import (
    RegisterView, LoginView, ProfileView,
    SendResetCodeView, VerifyResetCodeView,
    ResetPasswordWithTokenView, LogoutView
)

urlpatterns = [
    path('account/register/', RegisterView.as_view()),
    path('account/login/', LoginView.as_view()),
    path('account/profile/', ProfileView.as_view()),
    path('account/logout/', LogoutView.as_view()),
    path('account/password/send-reset-code/', SendResetCodeView.as_view()),
    path('account/password/verify-code/', VerifyResetCodeView.as_view()),
    path('account/password/reset/', ResetPasswordWithTokenView.as_view()),
]