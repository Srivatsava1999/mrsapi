from datetime import datetime, timedelta, time
from django.utils.timezone import make_aware
from django.db import transaction
from Booking.models import ShowDirectory
from Movie.models import MovieDirectory
from Theatre.models import ScreenDirectory

class Services:
    @staticmethod
    def show_schedular(movie_id, theatre_id, release_date):
        release_date=datetime.strptime(release_date, "%Y-%m-%d").date()
        release_date=make_aware(datetime.combine(release_date, datetime.min.time()))
        movie=MovieDirectory.objects.get(movieId=movie_id)
        movie_duration=timedelta(minutes=int(movie.duration))
        unavailable_screens=ShowDirectory.objects.filter(dateTime=release_date).values_list("screenId_id", flat=True)
        available_screens=ScreenDirectory.objects.filter(theatreId=theatre_id).exclude(
            screenId__in=unavailable_screens
        )
        print(available_screens)
        if not available_screens:
            return {"error":"No available screens for scheduling"}
        initial_time=time(9,0)
        buffer_time=timedelta(minutes=15)
        new_shows=[]
        current_time=datetime.combine(release_date.date(),initial_time)
        show_type_ids=[1,2,3,4]
        for show_type_id in show_type_ids:
            start_time=current_time.time()
            end_time=(current_time+movie_duration).time()
            if end_time>=time(23, 50):
                break
            new_show=ShowDirectory(
                movieId_id=movie_id,
                screenId=available_screens[0],
                theatreId_id=theatre_id,
                showTypeId_id=show_type_id,
                startTime=start_time,
                endTime=end_time,
                dateTime=release_date,
                houseFullFlag=False
                )
            new_shows.append(new_show)
            current_time+=movie_duration+buffer_time
        with transaction.atomic():
            ShowDirectory.objects.bulk_create(new_shows)
        return {"message":"Shows scheduled successfully"}
