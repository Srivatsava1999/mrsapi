from django.shortcuts import render
from social_django.utils import psa, load_backend, load_strategy
from rest_framework import generics, status
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.hashers import make_password
from Users.models import UserAccount
from Users.serializers import UserAccountSerializer
from Users.authentication import MRSAuthenticationclass

# Create your views here.
class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication,MRSAuthenticationclass]
    def post(self, request, format=None):
        try:
            refresh_token=request.data.get("refresh")
            MRSAuthenticationclass().blacklist_token(refresh_token)
            return Response(status=status.HTTP_205_RESET_CONTENT, data={"message":"Logged Out"})
        except Exception as e:
            return Response({"error": str(e)}, status=400)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data=super().validate(attrs)
        data.update({
            "user_id":self.user.id,
            "email": self.user.email,
            "role": self.user.role,
        })
        return data

class LoginView(TokenObtainPairView):
    serializer_class=CustomTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    queryset=UserAccount.objects.all()
    serializer_class=UserAccountSerializer
    permission_classes=[AllowAny]

    def perform_create(self, serializer):
        serializer.validated_data['password']=make_password(serializer.validated_data['password'])
        role=serializer.validated_data.get("role", UserAccount.CUSTOMER)
        if role not in [UserAccount.ADMIN, UserAccount.ENTERPRISE, UserAccount.CUSTOMER]:
            return ValidationError({"error": "Invalid Role"})
        serializer.save(role=role)

    def create(self, request, *args, **kwargs):
        response=super().create(request, *args, **kwargs)
        user=UserAccount.objects.get(email=request.data["email"])
        refresh=RefreshToken.for_user(user)
        response.data.update({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user_id": user.id,
            "email": user.email,
            "role": user.role
        })
        return response
    
class OAuth2SignupView(APIView):
    permission_classes=[AllowAny]
    # @psa('social:complete')
    def post(self, request, *args, **kwargs):
        backend_name=request.data.get('backend')
        access_token=request.data.get('access_token')
        if not backend_name or not access_token:
            return Response({"error":"Missing backend or access token"}, status=400)
        strategy=load_strategy(request)
        backend=load_backend(strategy, backend_name, redirect_uri=None)
        try:
            user=backend.do_auth(access_token)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        if user:
            user_obj,_= UserAccount.objects.get_or_create(
                email=user.email,
                defaults={
                    "name": user.name if hasattr(user, 'name') else "",
                    "role": UserAccount.CUSTOMER,
                    "is_active": True
                }
            )
            refresh=RefreshToken.for_user(user_obj)
            return Response({
                "refresh":str(refresh),
                "access":str(refresh.access_token),
                "user_id":user_obj.id,
                "email":user_obj.email
            })
        return Response({"error":"Invalid OAuth2 token"}, status=400)
