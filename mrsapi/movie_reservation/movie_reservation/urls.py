from django.contrib import admin
from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from Movie import views as MovieViews
from Theatre import views as TheatreViews
from Booking import views as BookingViews
from Users import views as UserViews
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/',MovieViews.MovieList.as_view()),
    path('movies/<int:pk>/', MovieViews.MovieDetail.as_view()),
    path('theatres/',TheatreViews.TheatreList.as_view()),
    path('theatres/<int:pk>/',TheatreViews.TheatreDetail.as_view()),
    path('theatre/<int:fk>/screen/', TheatreViews.ScreenList.as_view()),
    path('screen/<int:pk>/',TheatreViews.ScreenDetail.as_view()),
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
    path('logout/', UserViews.LogoutView.as_view(), name='token_blacklist'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh' ),
    # paths for unauthenticated users
    path('theatresall/', TheatreViews.TheatreViewAll.as_view()),
    path('theatresall/<int:pk>/', TheatreViews.TheatreViewSpecific.as_view()),
    path('theatresall/<int:fk>/showall/', BookingViews.ShowViewBy.as_view()),
    path('theatresall/<int:fk>/showall/<int:pk>', BookingViews.ShowViewSpecific.as_view()),
    path('screensall/<int:fk>/', TheatreViews.ScreenViewAll.as_view()),
    path('screensall/<int:fk>/seats/', TheatreViews.AudiView.as_view()),
    path('moviesall/', MovieViews.MovieViewAll.as_view()),
    path('movieall/<int:pk>/', MovieViews.MovieViewSpecific.as_view()),
    path('movieall/<int:fk>/showall/', BookingViews.ShowViewBy.as_view()),
    path('movieall/<int:fk>/showall/<int:pk>/', BookingViews.ShowViewSpecific.as_view()),
    path('showsall/', BookingViews.ShowViewAll.as_view()),
]
urlpatterns=format_suffix_patterns(urlpatterns)