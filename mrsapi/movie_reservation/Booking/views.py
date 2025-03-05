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
from rest_framework.permissions import IsAuthenticated, AllowAny
from Users.authentication import MRSAuthenticationclass
from movie_reservation.services import Services
# Create your views here.
class ShowViewAll(APIView):
    permission_classes=[AllowAny]
    def get(self, request, fk, format=None):
        shows=ShowDirectory.objects.select_related('movieId', 'theatreId').all()
        serializers=ShowDirectorySerializer(shows, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

class ShowViewBy(APIView):
    permission_classes=[AllowAny]
    def get(self, request, fk, format=None):
        if "movie" in request.path:
            shows=ShowDirectory.objects.select_related('movieId','theatreId').filter(movieId=fk)
        elif "theatre" in request.path:
            shows=ShowDirectory.objects.select_related('movieId','theatreId').filter(theatreId=fk)
        serializers=ShowDirectorySerializer(shows, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK) 

class ShowViewSpecific(APIView):
    permission_classes=[AllowAny]
    def read_show(self, pk):
        try:
            return ShowDirectory.objects.select_related('movieId','theatreId').get(showId=pk)
        except ShowDirectory.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        show=self.read_show(pk)
        serializer=ShowDirectorySerializer(show)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ShowList(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication,MRSAuthenticationclass]
    def get(self, request, fk, format=None):
        if "movie" in request.path:
            shows=ShowDirectory.objects.select_related('movieId','theatreId').filter(movieId=fk)
        elif "theatre" in request.path:
            shows=ShowDirectory.objects.select_related('movieId','theatreId').filter(theatreId=fk)
        serializers=ShowDirectorySerializer(shows, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, fk, format=None):
        data=request.data
        movie_id=data.get("movieId")
        theatre_id=data.get("theatreId")
        release_date=data.get("releaseDate")
        owner=request.headers.get("X-User-Id")
        user=UserAccount.objects.get(id=owner)
        if user.role!=UserAccount.CUSTOMER:
            if not all([movie_id, theatre_id, release_date]):
                return Response({"error":"Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                result=Services.show_schedular(
                    movie_id=movie_id,
                    theatre_id=theatre_id,
                    release_date=release_date
                )
                if "error" in result:
                    return Response(result, status=status.HTTP_400_BAD_REQUEST)
                return Response(result, status=status.HTTP_201_CREATED)
            except MovieDirectory.DoesNotExist:
                return Response({"error":"Movie not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                print(str(e))
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
            return ShowDirectory.objects.select_related('movieId','theatreId').get(showId=pk)
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