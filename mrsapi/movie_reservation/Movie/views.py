from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Movie.serializers import MovieDirectorySerializer
from Movie.models import MovieDirectory
from django.http import Http404
from Users.models import UserAccount
# Create your views here.

class MovieList(APIView):    
    def get(self, request, format=None):
        movies=MovieDirectory.objects.all()
        serializer=MovieDirectorySerializer(movies, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        if request.user.role!=UserAccount.CUSTOMER:
            serializer=MovieDirectorySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":"Customers can't write movies"}, status=status.HTTP_403_FORBIDDEN)
    
class MovieDetail(APIView):
    def read_movie(self, pk):
        try:
            return MovieDirectory.objects.get(movieId=pk)
        except MovieDirectory.DoesNotExist:
            raise Http404
    def write_movie(self, pk, user):
        try:
            if user.role!=UserAccount.CUSTOMER:
                return MovieDirectory.objects.get(movieId=pk)
            else:
                raise Http404
        except MovieDirectory.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        movie=self.read_movie(pk)
        serializer=MovieDirectorySerializer(movie)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        movie=self.write_movie(pk, request.user)
        serializer=MovieDirectorySerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        movie=self.write_movie(pk, request.user)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
