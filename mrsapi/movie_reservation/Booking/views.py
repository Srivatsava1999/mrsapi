from django.shortcuts import render
from django.db import transaction, IntegrityError
from django.core.cache import cache
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from Booking.models import ShowDirectory, BookingDirectory
from Booking.serializers import ShowDirectorySerializer, BookingDirectorySerializer

# Create your views here.

class ShowList(APIView):
    def get(self, request, fk, format=None):
        if "movie" in request.path:
            shows=ShowDirectory.objects.filter(movieId=fk)
        elif "theatre" in request.path:
            shows=ShowDirectory.objects.filter(theatreId=fk)
        serializers=ShowDirectorySerializer(shows, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    
    def post(self, request, fk, format=None):
        serializers=ShowDirectorySerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data ,status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ShowDetail(APIView):
    def get_show(self, pk):
        try:
            return ShowDirectory.objects.get(showId=pk)
        except:
            raise Http404
    
    def get(self, request, fk, pk, format=None):
        show=self.get_show(pk=pk)
        serializers=ShowDirectorySerializer(show)
        return Response(serializers.data, status=status.HTTP_202_ACCEPTED)
    
    def put(self, request, fk, pk, format=None):
        show=self.get_show(pk=pk)
        serializers=ShowDirectorySerializer(show, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, fk, pk, format=None):
        show=self.get_show(pk=pk)
        show.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class BookingList(APIView):
    def get(self, request, format=None):
        bookings=BookingDirectory.objects.all()
        serializers=BookingDirectorySerializer(bookings, many=True)
        return Response(serializers.data, status=status.HTTP_202_ACCEPTED)
    
    def post(self, request, format=None):
        serializers=BookingDirectorySerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BookingDetail(APIView):
    def get_booking(self, pk):
        try:
            return BookingDirectory.objects.get(bookingId=pk)
        except:
            raise Http404
    

    def get(self, request, pk, format=None):
        booking=self.get_booking(pk=pk)
        serializers=BookingDirectorySerializer(booking)
        return Response(serializers.data, status=status.HTTP_202_ACCEPTED)
    
    def put(self, request, pk, format=None):
        booking=self.get_booking(pk=pk)
        serializers=BookingDirectorySerializer(booking, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        booking=self.get_booking(pk=pk)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)