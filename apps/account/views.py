from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser, PasswordResetCode
from .serializers import RegisterSerializer, LoginSerializer, ProfileSerializer
from django.core.mail import send_mail
import secrets, random


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": status.HTTP_201_CREATED,
                "message": "User registered successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Validation failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)

            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "user_id": user.id,
                    "email": user.email,
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                }, status=status.HTTP_200_OK)

            return Response({
                "status": status.HTTP_401_UNAUTHORIZED,
                "success": False,
                "message": "Invalid credentials."
            }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Login failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Profile updated successfully",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "status": status.HTTP_400_BAD_REQUEST,
            "success": False,
            "message": "Profile update failed",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class SendResetCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Email is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        code = str(random.randint(100000, 999999))
        PasswordResetCode.objects.create(email=email, code=code)

        send_mail(
            "Password Reset Code",
            f"Your code is: {code}",
            "no-reply@paakhi.com",
            [email],
            fail_silently=True,
        )

        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Reset code sent"
        }, status=status.HTTP_200_OK)


class VerifyResetCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        try:
            reset = PasswordResetCode.objects.filter(email=email, code=code, is_used=False).latest("created_at")
        except PasswordResetCode.DoesNotExist:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Invalid or expired code"
            }, status=status.HTTP_400_BAD_REQUEST)

        if reset.is_expired():
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Verification code has expired."
            }, status=status.HTTP_400_BAD_REQUEST)

        reset.is_used = True
        reset.reset_token = secrets.token_hex(16)
        reset.save()

        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Verification successful.",
            "data": {
                "reset_token": reset.reset_token
            }
        }, status=status.HTTP_200_OK)


class ResetPasswordWithTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get("reset_token")
        password = request.data.get("password")
        confirm = request.data.get("confirm_password")

        if password != confirm:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Passwords do not match"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            reset = PasswordResetCode.objects.get(reset_token=token, is_used=True)
        except PasswordResetCode.DoesNotExist:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Invalid reset token"
            }, status=status.HTTP_400_BAD_REQUEST)

        if reset.is_expired():
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Reset token has expired."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=reset.email)
        except CustomUser.DoesNotExist:
            return Response({
                "status": status.HTTP_404_NOT_FOUND,
                "success": False,
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)

        user.set_password(password)
        user.save()

        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Password has been reset successfully."
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.data.get("refresh")
        if not token:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Refresh token is required."
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            RefreshToken(token).blacklist()
            return Response({
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Logout successful."
            }, status=status.HTTP_200_OK)
        except Exception:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "success": False,
                "message": "Invalid token or token already blacklisted."
            }, status=status.HTTP_400_BAD_REQUEST)
