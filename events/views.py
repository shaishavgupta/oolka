from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from .models import Event, Booking
from .serializers import EventSerializer, BookingSerializer
from rest_framework.response import Response
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
from rest_framework import status
from users.models import User

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
        event_id = kwargs.get('pk')
        user_id = request.data.get('user_id')
        tickets = request.data.get('tickets')

        ## checks event is valid
        event_qs = Event.objects.filter(id=event_id)
        if not event_qs.exists() or not event_qs.first().is_valid():
            return Response({"message": "invalid event"}, status=status.HTTP_400_BAD_REQUEST)
        event = event_qs.first()
        
        ## have required number of tickets available
        if event.available_tickets < tickets:
            return Response({'status': 'Not enough tickets available'}, status=400)
        
        ## user valid
        user_qs = User.objects.filter(id=user_id)
        if not user_qs.exists() or not user_qs.first().is_valid():
            return Response({"message": "invalid user"}, status=status.HTTP_400_BAD_REQUEST)

        ## distributed locks
        lock_id = 'lock:event:' + str(event_id)
        acquire_lock = cache.add(lock_id, 'true', DEFAULT_TIMEOUT)

        if acquire_lock:
            try:
                event.refresh_from_db()
                if event.available_tickets >= tickets:
                    event.price = event.price + 5
                    event.available_tickets -= tickets

                    booking = Booking.objects.create(
                        event_id=event_id,
                        user_id=user_id,
                        tickets=tickets,
                        price = event.price
                    )

                    event.save()
                    return Response({'status': 'Booking successful', "data":self.serializer_class(booking).data})
                else:
                    return Response({'status': 'Not enough tickets available'}, status=400)
            finally:
                cache.delete(lock_id)  # Release the lock

        else:
            return Response({'status': 'Tickets are being booked, please try again later'}, status=429)

        

    