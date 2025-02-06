from django.contrib import admin
from Booking.models import C_ShowType,ShowDirectory,BookingDirectory

# Register your models here.
class ShowAdmin(admin.ModelAdmin):
    ist_display = ('showTypeId', 'showType')
    list_filter = ('showTypeId',)
    search_fields = ('showType',)

admin.site.register(C_ShowType,ShowAdmin)
admin.site.register(ShowDirectory)
admin.site.register(BookingDirectory)