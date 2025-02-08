from django.db import models

# Create your models here.
class C_SeatType(models.Model):
    SEATTYPES={
        1 : "Regular",
        2 : "Premium",
    }
    seatTypeId=models.IntegerField(primary_key=True, choices=SEATTYPES.items(),default=1)
    
    @property
    def seatType(self):
        return self.SEATTYPES.get(self.seatTypeId, "unknown")
    
    def __str__(self):
        return self.seatType

class TheatreDirectory(models.Model):
    theatreId=models.AutoField(primary_key=True)
    theatreName=models.CharField(max_length=75)
    address=models.CharField(max_length=100)
    locationCity=models.CharField(max_length=75)
    locationState=models.CharField(max_length=75)

    def __str__(self):
        return self.theatreName
    

class ScreenDirectory(models.Model):
    screenId=models.AutoField(primary_key=True)
    screenNum=models.IntegerField()
    capacity=models.IntegerField()
    theatreId=models.ForeignKey(TheatreDirectory, on_delete=models.CASCADE)

    def __str__(self):
        return f"Screen {self.screenNum} - Theatre {self.theatreId.theatreName}"

class SeatMaster(models.Model):
    seatId=models.AutoField(primary_key=True)
    seatName=models.CharField(max_length=10)
    seatPrice=models.IntegerField()
    screenId=models.ForeignKey(ScreenDirectory, on_delete=models.CASCADE)
    seatTypeId=models.ForeignKey(C_SeatType, on_delete=models.CASCADE, default=1)
    seatRow=models.CharField(max_length=2, default='zx')
    seatCol=models.IntegerField(default=0)

    def __str__(self):
        return self.seatName



