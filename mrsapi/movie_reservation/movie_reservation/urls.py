"""
URL configuration for movie_reservation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from Movie import views as MovieViews
from Theatre import views as TheatreViews
from Booking import views as BookingViews
from Users import views as UserViews
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/',MovieViews.MovieList.as_view()),
    path('movies/<int:pk>/', MovieViews.MovieDetail.as_view()),
    path('theatres/',TheatreViews.TheatreList.as_view()),
    path('theatres/<int:pk>/',TheatreViews.TheatreDetail.as_view()),
    path('theatre/<int:fk>/screen/', TheatreViews.ScreenList.as_view()),
    path('theatre/<int:fk>/screen/<int:pk>/',TheatreViews.ScreenDetail.as_view()),
    path('screen/<int:fk>/seats/',TheatreViews.SeatList.as_view()),
    path('screen/<int:fk>/seats/<int:pk>',TheatreViews.SeatDetail.as_view()),
    path('theatre/<int:fk>/show/', BookingViews.ShowList.as_view()), # Bulk GET or POST(showschedularservice running) Request if the request shows by theatre
    path('movie/<int:fk>/show/', BookingViews.ShowList.as_view()), # Bulk GET or POST Request if the request shows by movie
    path('theatre/<int:fk>/show/<int:pk>/', BookingViews.ShowDetail.as_view()), # Specific GET or PUT or DELETE Request if the request shows by theatre
    path('movie/<int:fk>/show/<int:pk>/',BookingViews.ShowDetail.as_view()), # Specific GET or PUT or DELETE Request if the request shows by movie
    path('register/', UserViews.RegisterView.as_view()),
    path('login/', UserViews.LoginView.as_view()),
    path('oauth2-login/', UserViews.OAuth2SignupView.as_view()),
    path('auth/', include('social_django.urls', namespace='social')),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
]
urlpatterns=format_suffix_patterns(urlpatterns)