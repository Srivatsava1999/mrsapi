from django.contrib import admin
from Theatre.models import TheatreDirectory
from Theatre.models import ScreenDirectory
from Theatre.models import SeatMaster
from Theatre.models import C_SeatType

# Register your models here.
admin.site.register(TheatreDirectory)
admin.site.register(ScreenDirectory)
admin.site.register(SeatMaster)
admin.site.register(C_SeatType)