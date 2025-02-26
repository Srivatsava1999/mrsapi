from rest_framework_simplejwt.authentication import JWTAuthentication
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
            refresh_token=request.data.get("refresh")
            user=super().authenticate(request)
            if user:
                if self.is_blacklist(refresh_token):
                    raise AuthenticationFailed("Token is blacklisted")
                return user
        except AuthenticationFailed as e:
            raise e
        except Exception as e:
            raise e
        return None