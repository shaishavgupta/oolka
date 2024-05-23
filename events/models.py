from django.core.cache import cache
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models
from users.models import User
from django.conf import settings

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=30, blank=False, null=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE, serialize=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, serialize=False)
    is_active = models.BooleanField(default=True, blank=False, null=False, serialize=False)
    total_tickets = models.BigIntegerField(null=False, blank=False)
    available_tickets = models.BigIntegerField(null=False, blank=False)
    lat = models.FloatField(null=False, blank=False, serialize=False)
    lng = models.FloatField(null=False, blank=False, serialize=False)
    price = models.FloatField(null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    
    def __str__(self):
        return f'{self.date}-{self.name}-{self.is_active}'

    def is_valid(self):
        return self.available_tickets > 0 and self.available_tickets <= self.total_tickets and self.is_active and self.date > timezone.now().date()
    
@receiver(post_save, sender=Event)
def set_event_tickets(sender, instance, created, **kwargs):
    cache.set(f'event_{instance.id}', instance.available_tickets)

@receiver(pre_save, sender=Event)
def check_tickets(sender, instance, **kwargs):
    if instance.available_tickets > instance.total_tickets:
        raise ValidationError("Available tickets cannot be greater than total tickets")



class Booking(models.Model):
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, null=False, blank=False, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, serialize=False)
    is_active = models.BooleanField(default=True, blank=False, null=False, serialize=False)
    price = models.FloatField(null=False, blank=False)
    tickets = models.BigIntegerField(null=False, blank=False)

    def __str__(self):
        return f'{self.user.email}-{self.event.name}-{self.is_active}'

    def is_valid(self):
        return self.is_active

@receiver(pre_save, sender=Booking)
def validate(sender, instance, **kwargs):
    if instance.price <= 0:
        raise ValidationError("Price cannot be less than or equal to 0")

    if not instance.user.is_valid():
        raise ValidationError("User is not active")

    if not instance.event.is_valid():
        raise ValidationError("Event is not active")