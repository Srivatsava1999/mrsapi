from django.shortcuts import render
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from Theatre.models import TheatreDirectory, ScreenDirectory, SeatMaster
from Theatre.serializers import TheatreDirectorySerializer, ScreenDirectorySerializer, SeatMasterSerializer

# Create your views here.
class TheatreList(APIView):    
    def get(self, request, format=None):
        theatres=TheatreDirectory.objects.all()
        serializer=TheatreDirectorySerializer(theatres, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer=TheatreDirectorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TheatreDetail(APIView):
    def get_theatre(self, pk):
        try:
            return TheatreDirectory.objects.get(theatreId=pk)
        except TheatreDirectory.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        theatre=self.get_theatre(pk)
        serializer=TheatreDirectorySerializer(theatre)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        theatre=self.get_theatre(pk)
        serializer=TheatreDirectorySerializer(theatre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        theatre=self.get_theatre(pk)
        theatre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ScreenList(APIView):
    def get(self, request, fk, format=None):
        screens=ScreenDirectory.objects.filter(theatreId=fk)
        serializer=ScreenDirectorySerializer(screens, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):
        data=request.data.copy()
        data[theatreId]=int(fk)
        serializer=ScreenDirectorySerializer(data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ScreenDetail(APIView):
    def get_screen(self, pk):
        try:
            return ScreenDirectory.objects.get(screenId=pk)
        except ScreenDirectory.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        screen=self.get_screen(pk)
        serializer=ScreenDirectorySerializer(screen)
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        screen=self.get_screen(pk)
        serializer=ScreenDirectorySerializer(screen, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,format=None):
        screen=self.get_screen(pk)
        screen.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        