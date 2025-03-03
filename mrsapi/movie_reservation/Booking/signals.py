from django.db.models.signals import post_migrate
from django.dispatch import receiver
from Booking.models import C_ShowType

@receiver(post_migrate)
def create_show_types(sender, **kwargs):
    if sender.name == "Booking":
        for key, value in C_ShowType.SHOWTYPES.items():
            C_ShowType.objects.get_or_create(showTypeId=key)
