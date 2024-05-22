from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.views import APIView
from .models import Event, Booking
from users.models import User
from .serializers import EventSerializer, BookingSerializer
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache


# Create your views here.
class EventView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

    def get_queryset(self):
        queryset = Event.objects.all()
        if self.kwargs.get('pk') is not None:
            queryset = queryset.filter(id=self.kwargs.get('pk'))
        return queryset

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)



class BookingView(generics.ListCreateAPIView):
    serializer_class = BookingSerializer

    def post(self, request, *args, **kwargs):

        event_id = self.kwargs.get('pk')
        if event_id is None:
            return Response({"message": "event_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        event_qs = Event.objects.filter(id=event_id)
        if not event_qs.exists() or not event_qs.first().isValid():
            return Response({"message": "invalid event"}, status=status.HTTP_400_BAD_REQUEST)
        event = event_qs.first()

        user_id = request.data.get('user_id')
        if user_id is None:
            return Response({"message": "user_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        user_qs = User.objects.filter(id=user_id)
        if not user_qs.exists() or not user_qs.first().isValid():
            return Response({"message": "invalid user"}, status=status.HTTP_400_BAD_REQUEST)
        
        ## distributed lock
        lock_id = f"event_{event_id}"
        available_tickets = cache.get(lock_id)
        if available_tickets == 0:
            return Response({"message": "no tickets available"}, status=status.HTTP_400_BAD_REQUEST)
        
        cache.set(lock_id, available_tickets - 1)
        booking = Booking.objects.create(event=event, user_id=user_id, price=event.price)
        if booking is None or not booking.isValid():
            cache.set(lock_id, available_tickets)
            return Response({"message": "booking failed"}, status=status.HTTP_400_BAD_REQUEST)

        ## update event price and available tickets
        event.available_tickets = available_tickets - 1
        event.price = event.price + 5
        event.save()
        
        return Response(self.serializer_class(booking).data)
        
        

    