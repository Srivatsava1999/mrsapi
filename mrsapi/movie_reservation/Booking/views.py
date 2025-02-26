from django.shortcuts import render
from django.db import transaction, IntegrityError
from django.core.cache import cache
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from Booking.models import ShowDirectory, BookingDirectory, C_ShowType
from Booking.serializers import ShowDirectorySerializer, BookingDirectorySerializer
from Theatre.models import ScreenDirectory, TheatreDirectory, SeatMaster, C_SeatType
from Movie.models import MovieDirectory
from datetime import datetime, timedelta, time
from django.utils.timezone import make_aware
from Users.models import UserAccount
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from Users.authentication import MRSAuthenticationclass
# Create your views here.

class ShowList(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication,MRSAuthenticationclass]
    def get(self, request, fk, format=None):
        if "movie" in request.path:
            shows=ShowDirectory.objects.filter(movieId=fk)
        elif "theatre" in request.path:
            shows=ShowDirectory.objects.filter(theatreId=fk)
        serializers=ShowDirectorySerializer(shows, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, fk, format=None):
        data=request.data
        movie_id=data.get("movieId")
        theatre_id=data.get("theatreId")
        release_date=data.get("releaseDate")
        show_types=data.get("showTypes",[])
        if data.user.role!=UserAccount.CUSTOMER:
            if not all([movie_id, theatre_id, release_date, show_types]):
                return Response({"error":"Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                release_date=datetime.strptime(release_date, "%Y-%m-%d").date()
                release_date=make_aware(datetime.combine(release_date, datetime.min.time()))
                movie=MovieDirectory.objects.get(movieId=movie_id)
                runtime_minutes=int(movie.duration)
                movie_duration=timedelta(minutes=runtime_minutes)
                unavailable_screens = ShowDirectory.objects.filter(dateTime=release_date).values_list('screenId_id', flat=True)

                available_screens=ScreenDirectory.objects.filter(theatreId=theatre_id).exclude(
                    screenId__in=unavailable_screens
                )
                if not available_screens.exists():
                    return Response({"error":"No available screens for scheduling"},status=status.HTTP_400_BAD_REQUEST)
                
                initia_time=time(9,0)
                buffer_time=timedelta(minutes=15)

                new_shows=[]
                current_time=datetime.combine(datetime.today(), initia_time)
                for show_type_id in show_types:
                    start_time=current_time.time()
                    end_time=(current_time+movie_duration).time()

                    if end_time>=time(23,50):
                        break

                    new_show=ShowDirectory(
                        movieId_id=movie_id,
                        screenId=available_screens[0],
                        theatreId_id=theatre_id,
                        showTypeId_id=show_type_id,
                        startTime=start_time,
                        endTime=end_time,
                        dateTime=release_date,
                        houseFullFlag=False
                    )
                    new_shows.append(new_show)
                    current_time+=movie_duration+buffer_time
                
                with transaction.atomic():
                    ShowDirectory.objects.bulk_create(new_shows)
                
                return Response({"message": "Shows scheduled successfully"}, status=status.HTTP_201_CREATED)
            
            except MovieDirectory.DoesNotExist:
                return Response({"error":"Movie not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error":"Customers can't write shows"}, status=status.HTTP_403_FORBIDDEN)

class ShowDetail(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication,MRSAuthenticationclass]
    def write_show(self, pk, user):
        try:
            show=ShowDirectory.objects.get(showId=pk)
            if user.role==UserAccount.ADMIN or show.theatreId.owner==user:
                return show
            raise Http404
        except:
            raise Http404
    def read_show(self, pk):
        try:
            return ShowDirectory.objects.get(showId=pk)
        except ShowDirectory.DoesNotExist:
            raise Http404
    
    def get(self, request, fk, pk, format=None):
        show=self.read_show(pk)
        serializers=ShowDirectorySerializer(show)
        return Response(serializers.data, status=status.HTTP_202_ACCEPTED)
    
    def put(self, request, fk, pk, format=None):
        show=self.write_show(pk=pk)
        serializers=ShowDirectorySerializer(show, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, fk, pk, format=None):
        show=self.write_show(pk=pk)
        show.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class BookingList(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication,MRSAuthenticationclass]
    def get(self, request, format=None):
        user=request.user
        if user.role==UserAccount.ADMIN:
            bookings=BookingDirectory.objects.all()
        else:
            bookings=BookingDirectory.objects.filter(showId_theatreId_owner=user)
        serializers=BookingDirectorySerializer(bookings, many=True)
        return Response(serializers.data, status=status.HTTP_202_ACCEPTED)
    
    def post(self, request, format=None):
        serializers=BookingDirectorySerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BookingDetail(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication,MRSAuthenticationclass]
    def get_booking(self, pk, user):
        try:
            booking=BookingDirectory.objects.get(bookingId=pk)
            if user.role==UserAccount.ADMIN or booking.showId.theatreId.owner==user:
                return booking
            raise Http404
        except:
            raise Http404
    

    def get(self, request, pk, format=None):
        booking=self.get_booking(pk, request.user)
        serializers=BookingDirectorySerializer(booking)
        return Response(serializers.data, status=status.HTTP_202_ACCEPTED)
    
    def put(self, request, pk, format=None):
        booking=self.get_booking(pk, request.user)
        serializers=BookingDirectorySerializer(booking, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        booking=self.get_booking(pk=pk)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)