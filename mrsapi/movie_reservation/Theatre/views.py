from django.shortcuts import render
from django.db import transaction, IntegrityError
from django.core.cache import cache
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from Theatre.models import TheatreDirectory, ScreenDirectory, SeatMaster
from Theatre.serializers import TheatreDirectorySerializer, ScreenDirectorySerializer, SeatMasterSerializer
from Users.models import UserAccount
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from Users.authentication import MRSAuthenticationclass

# Create your views here.
class TheatreList(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication,MRSAuthenticationclass]   
    def get(self, request, format=None):
        theatres=TheatreDirectory.objects.all()
        serializer=TheatreDirectorySerializer(theatres, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        user=request.user
        owner=request.headers.get("X-User-Id")
        if user.role == UserAccount.CUSTOMER:
            return Response({"error":"Customers can't create theatres"})
        serializer=TheatreDirectorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors, request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TheatreDetail(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication,MRSAuthenticationclass]
    def write_theatre(self, pk, user, owner):
        try:
            if user.role == UserAccount.ADMIN:
                return TheatreDirectory.objects.get(theatreId=pk)
            else:
                return TheatreDirectory.objects.get(theatreId=pk,owner=owner)
        except TheatreDirectory.DoesNotExist:
            raise Http404
    def read_theatre(self, pk):
        try:
            return TheatreDirectory.objects.get(theatreId=pk)
        except TheatreDirectory.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        theatre=self.read_theatre(pk)
        serializer=TheatreDirectorySerializer(theatre)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        owner=request.headers.get("X-User-Id")
        theatre=self.write_theatre(pk, request.user, owner)
        serializer=TheatreDirectorySerializer(theatre, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=owner)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        owner=request.headers.get("X-User-Id")
        theatre=self.write_theatre(pk, request.user, owner)
        theatre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ScreenList(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication,MRSAuthenticationclass]
    def get(self, request, fk, format=None):
        screens=ScreenDirectory.objects.filter(theatreId=fk)
        serializer=ScreenDirectorySerializer(screens, many=True)
        return Response(serializer.data)
    def post(self, request, fk,format=None):
        owner=request.headers.get("X-User-Id")
        user=UserAccount.objects.get(id=owner)
        if user.role==UserAccount.CUSTOMER:
            print(user.role,"issue with user class")
            return Response({"error":"Customers can't create screens"}, status=status.HTTP_403_FORBIDDEN)
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
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication,MRSAuthenticationclass]
    def write_screen(self, pk, user):
        try:
            if user.role==UserAccount.ADMIN:
                return ScreenDirectory.objects.get(screenId=pk)
            return ScreenDirectory.objects.get(screenId=pk, theatreId__owner=user)
        except ScreenDirectory.DoesNotExist:
            raise Http404
    def read_screen(self, pk):
        try:
            return ScreenDirectory.objects.get(screenId=pk)
        except:
            raise Http404
    
    def get(self, request, pk, fk, format=None):
        screen=self.read_screen(pk)
        serializer=ScreenDirectorySerializer(screen)
        return Response(serializer.data)
    def put(self, request, pk,fk, format=None):
        owner=request.headers.get("X-User-Id")
        screen=self.write_screen(pk, request.user, owner)
        serializer=ScreenDirectorySerializer(screen, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk,fk,format=None):
        owner=request.headers.get("X-User-Id")
        screen=self.write_screen(pk, request.user)
        screen.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class SeatList(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication,MRSAuthenticationclass]
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
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication,MRSAuthenticationclass]
    def write_seat(self,pk, user):
        try:
            if user.role==UserAccount.ADMIN:
                return SeatMaster.objects.get(seatId=pk)
            return SeatMaster.objects.get(seatId=pk, screenId__theatreId__owner=user)
        except SeatMaster.DoesNotExist:
            raise Http404
    def read_seat(self,pk):
        try:
            return SeatMaster.objects.get(seatId=pk)
        except SeatMaster.DoesNotExist:
            raise Http404
        
    def get(self,request,pk,format=None):
        seat=self.read_seat(pk)
        serializer=SeatMasterSerializer(seat)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self, request, pk,fk, format=None):
        seat=self.write_seat(pk, request.user)
        serializer=SeatMasterSerializer(seat, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk,fk,format=None):
        seat=self.write_seat(pk, request.user)
        seat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
            