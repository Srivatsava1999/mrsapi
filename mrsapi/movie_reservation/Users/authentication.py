from rest_framework_simplejwt.authentication import JWTAuthentication
from Users.models import UserAccount
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from rest_framework.exceptions import AuthenticationFailed


class RedisTokenBlacklist:
    def blacklist_token(self, token):
        cache.set(token, "blacklist", timeout=60*60*24) #1 day
    
    def is_blacklist(self, token):
        if cache.get(token):
            return True
        return False
    
class MRSAuthenticationclass(JWTAuthentication, RedisTokenBlacklist):
    def authenticate(self, request):
        try:
            refresh_token=request.headers.get("X-Refresh-Token")
            user, validated_token=super().authenticate(request)
            if user:
                if self.is_blacklist(refresh_token):
                    raise AuthenticationFailed("Token is blacklisted")
                return (user, validated_token)
        except AuthenticationFailed as e:
            if not self.is_blacklist(refresh_token):
                try:
                    new_token=RefreshToken(refresh_token)
                    new_access_token=str(new_token.access_token)
                    user_id=new_token.payload["user_id"]
                    user=UserAccount.objects.get(id=user_id)
                    return (user, new_access_token)
                except Exception:
                    raise AuthenticationFailed("Refresh token is invalid")
            raise AuthenticationFailed("Token is blacklisted")
        except Exception as e:
            raise e
        return None