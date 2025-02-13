from django.db import models
from Movie.models import MovieDirectory
from Theatre.models import TheatreDirectory, ScreenDirectory, SeatMaster

# Create your models here.
class C_ShowType(models.Model):
    SHOWTYPES={
        1 : 'Morning Show',
        2 : 'Matinee Show',
        3 : 'First Show',
        4 : 'Second Show',
    }
    showTypeId=models.IntegerField(primary_key=True,choices=SHOWTYPES.items(), default=1)

    @property
    def showType(self):
        # return self.SHOWTYPES[self.showTypeId]
        return self.SHOWTYPES.get(self.showTypeId, "unkown")
    # The @property file makes it so that the function acts as an attribute, so C_ShowType.showType is an attribute of the class.
    
    def __str__(self):
        return self.showType
    
class ShowDirectory(models.Model):
    showId=models.AutoField(primary_key=True)
    movieId=models.ForeignKey(MovieDirectory, on_delete=models.CASCADE)
    screenId=models.ForeignKey(ScreenDirectory, on_delete=models.CASCADE)
    theatreId=models.ForeignKey(TheatreDirectory, on_delete=models.CASCADE)
    showTypeId=models.ForeignKey(C_ShowType, on_delete=models.CASCADE)
    startTime=models.TimeField()
    endTime=models.TimeField()
    dateTime=models.DateTimeField()
    houseFullFlag=models.BooleanField(default=False)

    class Meta:
        constraints=[models.UniqueConstraint(
            fields=['screenId','dateTime','showTypeId'],
            name='unique_show_per_screen_per_date'
        )]
    
    def save(self, *args, **kwargs):
        if ShowDirectory.objects.filter(
            screenId=self.screenId,
            dateTime=self.dateTime,
            showTypeId=self.showTypeId
            ).exists():
                raise IntegrityError("Show already scheduled for this screem on this data.")
        super().save(*args,**kwargs)
        

class BookingDirectory(models.Model):
    bookingId=models.AutoField(primary_key=True)
    seatID=models.ForeignKey(SeatMaster, on_delete=models.CASCADE)
    showId=models.ForeignKey(ShowDirectory, on_delete=models.CASCADE)
