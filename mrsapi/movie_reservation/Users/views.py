from django.shortcuts import render, redirect
from movie_reservation import settings
from social_django.utils import psa, load_backend, load_strategy
from rest_framework import generics, status
from django.core.cache import cache
from rest_framework.exceptions import AuthenticationFailed
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
from Users.serializers import UserAccountSerializer, AuthSerializer
from Users.authentication import MRSAuthenticationclass
from urllib.parse import urlencode
from typing import Dict, Any
import requests
GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'
LOGIN_URL = f'{settings.BASE_APP_URL}login/'
# Create your views here.
class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication,MRSAuthenticationclass]
    def post(self, request, format=None):
        try:
            refresh_token=request.headers.get("refresh")
            MRSAuthenticationclass().blacklist_token(refresh_token)
            return Response(status=status.HTTP_200_OK, data={"message":"Logged Out"})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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
    def post(self,request,*args, **kwargs):
        response=super().post(request,*args, **kwargs)
        response.data.update({
            "access": response.data["access"],
            "refresh": response.data["refresh"]
        })
        return Response(response.data)

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
    def get_user_info(self, access_token) -> Dict[str, Any]:
        response=requests.get(
            GOOGLE_USER_INFO_URL,
            params={"access_token":access_token}
        )
        if not response.ok:
            raise ValidationError('Could not get user info from Google')
        return response.json()

    def get_access_token(self,validated_data):
        domain=settings.BASE_API_URL
        redirect_uri=f'{domain}/oauth2-login/'
        code=validated_data.get('code')
        error=validated_data.get('error')
        if error or not code:
            params=urlencode({"error":error})
            return redirect(f'{LOGIN_URL}?{params}')
        data={
            "code":code,
            "client_id":settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY,
            "client_secret":settings.SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET,
            "redirect_uri":redirect_uri,
            "grant_type":"authorization_code"
        }
        response=requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)
        if not response.ok:
            raise ValidationError('could not get access token from google')
        return response.json()
    
    def get(self, request, *args, **kwargs):
        auth_serializer=AuthSerializer(data=request.GET)
        auth_serializer.is_valid(raise_exception=True)
        validated_data=auth_serializer.validated_data
        token_data=self.get_access_token(validated_data)
        backend_name='google-oauth2'
        access_token=token_data['access_token']
        if not access_token:
            return Response({"error":"Missing backend or access token"}, status=400)
        user_info=self.get_user_info(access_token)
        strategy=load_strategy(request)
        backend=load_backend(strategy, backend_name, redirect_uri=None)
        try:
            user=backend.do_auth(access_token)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        if user:
            user_obj,_= UserAccount.objects.get_or_create(
                email=user_info['email'],
                defaults={
                    "name": user_info['name'] if hasattr(user, 'name') else "",
                    "role": UserAccount.CUSTOMER,
                    "is_active": True
                }
            )
            refresh=RefreshToken.for_user(user_obj)
            frontend_url=f'{settings.BASE_APP_URL}/oauth2-success/'
            params=urlencode({
                "refresh":str(refresh),
                "access":str(refresh.access_token),
                "user_id":user_obj.id,
                "email":user_obj.email
            })
            return redirect(f"{frontend_url}?{params}")
        return Response({"error":"Invalid OAuth2 token"}, status=400)
    
