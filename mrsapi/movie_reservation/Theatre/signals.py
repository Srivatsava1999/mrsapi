from django.db.models.signals import post_migrate
from django.dispatch import receiver
from Theatre.models import C_SeatType

@receiver(post_migrate)
def create_seat_types(sender, **kwargs):
    if sender.name == "Theatre":
        for key, value in C_SeatType.SEATTYPES.items():
            C_SeatType.objects.get_or_create(seatTypeId=key)
