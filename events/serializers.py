from rest_framework import serializers
from .models import Event, Booking

class EventSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    
    def get_link(self, obj):
        return f"https://www.google.com/maps?q={obj.lat},{obj.lng}"

    class Meta:
        model = Event
        fields = '__all__'



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
