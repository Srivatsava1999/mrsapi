from django.db import models

# Create your models here.
class MovieDirectory(models.Model):
    movieId=models.AutoField(primary_key=True)
    movieTitle=models.CharField(max_length=100)
    duration=models.DurationField(help_text="Duration of the movie (HH:MM:SS format)")
    rating=models.CharField(max_length=75)
    release_date=models.DateField(max_length=75)

    def __str__(self):
        return self.movieTitle