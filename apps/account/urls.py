from django.urls import path
from .views import (
    RegisterView, LoginView, ProfileView,
    SendResetCodeView, VerifyResetCodeView,
    ResetPasswordWithTokenView, LogoutView
)

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('password/send-reset-code/', SendResetCodeView.as_view()),
    path('password/verify-code/', VerifyResetCodeView.as_view()),
    path('password/reset/', ResetPasswordWithTokenView.as_view()),
]