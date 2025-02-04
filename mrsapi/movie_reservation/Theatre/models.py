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