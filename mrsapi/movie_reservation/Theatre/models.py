from django.db import models

# Create your models here.
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
    DateTime=models.DateTimeField()
    screenNum=models.IntegerField()
    capacity=models.IntegerField()
    theatreId=models.ForeignKey(TheatreDirectory, on_delete=models.CASCADE)

    def __str__(self):
        return self.screenId

class SeatMaster(models.Model):
    SeatId=models.AutoField(primary_key=True)
    SeatName=models.CharField(max_length=10)
    SeatClass=models.CharField(max_length=75)
    SeatPrice=models.IntegerField()
    screenId=models.ForeignKey(ScreenDirectory, on_delete=models.CASCADE)

    def __str__(self):
        return self.SeatName
