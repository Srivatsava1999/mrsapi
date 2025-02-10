from django.shortcuts import render
from django.db import transaction, IntegrityError
from django.core.cache import cache
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
    def post(self, request, fk,format=None):
        serializer=ScreenDirectorySerializer(data=request.data)
        if serializer.is_valid():
            screenInstance=serializer.save()
            seatResponse = SeatList.seat_pop(screenInstance.screenId, screenInstance.capacity)
            return Response({
                "screen":serializer.data,
                "seat_creation":seatResponse.data
            },status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ScreenDetail(APIView):
    def get_screen(self, pk):
        try:
            return ScreenDirectory.objects.get(screenId=pk)
        except ScreenDirectory.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, fk, format=None):
        screen=self.get_screen(pk)
        serializer=ScreenDirectorySerializer(screen)
        return Response(serializer.data)
    def put(self, request, pk,fk, format=None):
        screen=self.get_screen(pk)
        serializer=ScreenDirectorySerializer(screen, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,fk,format=None):
        screen=self.get_screen(pk)
        screen.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class SeatList(APIView):
    def get(self, request, fk, format=None):
        seat_layout=cache.get(f"screen_{fk}")
        if seat_layout:
            return Response({"screenId": fk, "seat_layout": seat_layout}, status=status.HTTP_200_OK)
        seats=SeatMaster.objects.filter(screenId=fk)
        serializer=SeatMasterSerializer(seats, many=True)
        return Response(serializer.data)

    @staticmethod    
    def seat_pop(screenId : int, cap : int):
        rows = round(cap ** 0.5)
        cols = cap // rows
        left_over = cap - (cols * rows)

        premium_rows = rows // 5  # First X rows are premium 

        # Generate seat numbers
        seatnums = [[j + 1 for j in range(cols)] for _ in range(rows)]

            # Handle leftover seats
        if left_over < premium_rows:
            for l in range(left_over):
                seatnums[l].append(cols + 1)
        else:
            seatnums.append([j + 1 for j in range(left_over)])

            # Create SeatMaster compatible list
        seatmaster_objects = []
        seatLayoutDict={}

        for i, row in enumerate(seatnums):
            row_label = chr(65 + i)  # Convert row index to letter (A, B, C, ...)
            price = 40 if i < premium_rows else 30
            seat_type = 2 if price == 40 else 1  # Assign seat type based on price
            seatLayoutDict[row_label]=row
            for col_num in row:
                seatmaster_objects.append(
                    SeatMaster(
                        seatName=f"{row_label}{col_num}",
                        seatRow=row_label,
                        seatCol=col_num,
                        seatPrice=price,
                        seatTypeId_id=seat_type,  # ForeignKey requires _id suffix
                        screenId_id=screenId  # ForeignKey requires _id suffix
                    )
                )
        
        try:
            with transaction.atomic():
                SeatMaster.objects.bulk_create(seatmaster_objects)
                cache.set(f"screen_{screenId}",seatLayoutDict, timeout=None)
            return Response(
                {"message":"Seats Created!!", "screenId":screenId, "cached": True},
                status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response(
                {"message":"Database Error while Creating Seats !!", "details":str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response(
                {"message":"Don't know what the fuck went wrong !!", "details":str(e)},
                 status=status.HTTP_400_BAD_REQUEST)
        
class SeatDetail(APIView):
    def get_seat(self,pk):
        try:
            return SeatMaster.objects.get(seatId=pk)
        except SeatMaster.DoesNotExist:
            raise Http404
        
    def get(self,request,pk,format=None):
        seat=self.get_seat(self,pk)
        serializer=SeatMasterSerializer(seat)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self, request, pk,fk, format=None):
        seat=self.get_seat(pk)
        serializer=SeatMasterSerializer(seat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk,fk,format=None):
        seat=self.get_seat(pk)
        seat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
            