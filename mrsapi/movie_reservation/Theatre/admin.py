from django.contrib import admin
from Theatre.models import TheatreDirectory
from Theatre.models import ScreenDirectory
from Theatre.models import SeatMaster

# Register your models here.
admin.site.register(TheatreDirectory)
admin.site.register(ScreenDirectory)
admin.site.register(SeatMaster)