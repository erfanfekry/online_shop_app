from django.db.models.signals import pre_save

from .models import *
from django.dispatch import receiver
from django.db.models import signals

@receiver(signal=pre_save, sender=Product)
def calculate_new_price(sender, instance, **kwargs):
    instance.new_price = instance.price - instance.discount



