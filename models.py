from django.db import models

# Create your models here.
from django.conf import settings

# Custom User Model to replace the default Django User model
class CustomUser(models.Model):       #here you have 2 options to use AbstractUser or models.Model, we are using models.MOdel coz we want a whole customized User
    ROLE_CHOICES = [
        ('user', 'User'),
        ('tour_guide', 'Tour Guide'),
    ]
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_info = models.CharField(max_length=15)  # Assuming it's a phone number
    age = models.IntegerField()
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    user_id = models.AutoField(primary_key=True)
    REQUIRED_FIELDS=["name"]
    USERNAME_FIELD="name"
    
    def __str__(self):          #makes debugging simpler and improves readability in django admin and shell
        return self.name

# Tour Model representing the TOURS entity
class Tour(models.Model):
    tour_id = models.AutoField(primary_key=True)
    location = models.CharField(max_length=255)
    no_of_days = models.IntegerField()

    def __str__(self):
        return f"Tour to {self.location} for {self.no_of_days} days"

# Booking Model representing the BOOKINGS entity
class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="bookings")  # Many-to-One relationship with CustomUser
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="bookings")  # Many-to-One relationship with Tour
    booking_date = models.DateField()
    no_of_people = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    mode_of_payment = models.CharField(max_length=50)

    def __str__(self):
        return f"Booking {self.booking_id} by {self.user.name} for {self.tour.location}"

# Review Model representing the REVIEWS entity
class Review(models.Model):
    tour = models.ForeignKey('Tour', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField()  # Ratings from 1 to 5
    comment = models.TextField(blank=True, null=True)  # Optional text comment
    images = models.ImageField(upload_to='review_photos/', blank=True, null=True)  # Optional photo
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review {self.review_id} by {self.user.name} for {self.tour.location}"
