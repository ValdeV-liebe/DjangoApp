from .models import Album , Artist , Booking , Contact
from django.test import TestCase
from django.urls import reverse

# index page
class IndexPageTestCase(TestCase) :
    def test_index_page(self) :
        response = self.client.get(reverse('hello'))
        self.assertEqual(response.status_code , 200)

#Detail page
class DetailPageTestCase(TestCase) :
    
    def setUp(self) :
        impossible = Album.objects.create(title = "Transmission Impossible" , image = "/d.jpg")
        self.album =Album.objects.get(title = "Transmission Impossible")
    
    def test_detail_page_returns_200(self) :
        album_id = self.album.id
        response = self.client.get(reverse('detail' , args = (album_id,)))
        self.assertEqual(response.status_code , 200)
    
    def test_detail_page_returns_404(self) :
        album_id = self.album.id + 1
        response = self.client.get(reverse('detail' , args = (album_id,)))
        self.assertEqual(response.status_code , 404)

#Booking page
class BookingPageTestCase(TestCase) :
    def setUp(self) :
        Contact.objects.create(name = "Val" , email ="val@gmail.com")
        impossible = Album.objects.create(title = "Transmission Impossible" , image = "/d.jpg")
        journey = Artist.objects.create(name = "Big")
        impossible.artists.add(journey)
        self.contact = Contact.objects.get(name = "Val")
        self.album = Album.objects.get(title = "Transmission Impossible")
    
    def test_new_booking_is_registered(self) :
        old_bookings = Booking.objects.count()
        album_id = self.album.id
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(
            reverse(
                'detail' ,
                args =(album_id,)
            ) ,
            {
                    'name' : name ,
                    'email' : email
                }
            
        )
        new_bookings = Booking.objects.count()
        self.assertEqual(new_bookings , old_bookings + 1)