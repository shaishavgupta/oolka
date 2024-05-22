from django.test import TestCase
from datetime import datetime
from .models import Event, Booking
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from users.models import User


class TestEvent(TestCase):
    def setUp(self):
        authUser = get_user_model().objects.create(
            username='testuser',
            password='testuser',
        )
        self.event = Event.objects.create(
            name='Test Event',
            created_by=authUser,
            total_tickets = 100,
            available_tickets = 100,
            lat = 10.1,
            lng = 10.1,
            price = 100.1,
            date = '2021-08-01'
            )
    
    def test_event_creation(self):
        self.assertEqual(cache.get(f'event_{self.event.id}'), self.event.available_tickets)
    
    def test_event_tickets(self):
        self.assertLessEqual(self.event.total_tickets, self.event.available_tickets)


class TestBooking(TestCase):
    def setUp(self):
        authUser = get_user_model().objects.create(
            username='testuser',
            password='testuser',
        )

        self.event = Event.objects.create(
            name='Test Event',
            created_by=authUser,
            total_tickets = 100,
            available_tickets = 100,
            lat = 10.1,
            lng = 10.1,
            price = 100,
            date = datetime.now().date()
            )

        self.inactive_user = User.objects.create(
                name='testuser',
                email='testuser@example.com',
                is_active=False
            )

    def test_inactive_user_cannot_book(self):
        with self.assertRaises(ValidationError):
            Booking.objects.create(
                user=self.inactive_user,
                event=self.event,
                price=100
            )