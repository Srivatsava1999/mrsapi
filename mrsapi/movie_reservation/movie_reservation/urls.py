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
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from Movie import views as MovieViews
from Theatre import views as TheatreViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/',MovieViews.MovieList.as_view()),
    path('movies/<int:pk>/', MovieViews.MovieDetail.as_view()),
    path('theatres/',TheatreViews.TheatreList.as_view()),
    path('theatres/<int:pk>/',TheatreViews.TheatreDetail.as_view()),
    path('theatre/<int:fk>/screen/', TheatreViews.ScreenList.as_view()),
    path('theatre/<int:fk>/screen/<int:pk>/',TheatreViews.ScreenDetail.as_view())
]
urlpatterns=format_suffix_patterns(urlpatterns)