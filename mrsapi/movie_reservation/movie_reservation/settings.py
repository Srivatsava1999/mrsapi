from pathlib import Path
import django_redis
import os
from dotenv import load_dotenv
from datetime import timedelta
from corsheaders.defaults import default_headers
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=os.getenv("GOOGLE_OAUTH_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
BASE_APP_URL=os.getenv("BASE_APP_URL")
BASE_API_URL=os.getenv("BASE_API_URL")
SQL_ENGINE=os.getenv("SQL_ENGINE")
SQL_NAME=os.getenv("SQL_NAME")
SQL_USER= os.getenv("SQL_USER")
SQL_PASSWORD=os.getenv("SQL_PASSWORD")
SQL_HOST=os.getenv("SQL_HOST")
SQL_PORT=os.getenv("SQL_PORT")
CACHE_BACKEND=os.getenv("CACHE_BACKEND")
CACHE_LOCATION=os.getenv("CACHE_LOCATION")
DEBUG = True

ALLOWED_HOSTS = []

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000", 
]




INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'oauth2_provider',
    'social_django',
    'Movie',
    'Theatre',
    'Booking',
    'corsheaders',
    'Users',
]


REST_FRAMEWORK={
    'DEFAULT_AUTHENTICATION_CLASSES':(
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}
SIMPLE_JWT={
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=6),
}
AUTHENTICATION_BACKENDS=[
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_USER_MODEL = 'Users.UserAccount'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
CORS_ALLOW_HEADERS=list(default_headers)+[
    "x-refresh-token",
    "x-user-id",
]
ROOT_URLCONF = 'movie_reservation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'movie_reservation.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': SQL_ENGINE,
        'NAME': SQL_NAME,
        'USER': SQL_USER,
        'PASSWORD': SQL_PASSWORD,
        'HOST': SQL_HOST,
        'PORT': SQL_PORT,
    }
}
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",  # Use the service name "redis"
        "KEY_PREFIX": "",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            
            "KEY_FUNCTION": lambda key, _: key,
        }
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True



STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
