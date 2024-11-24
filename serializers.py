# serializers.py

from rest_framework import serializers
from .models import Tour, Review

class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'tour', 'user', 'rating', 'comment', 'images', 'created_at']
        read_only_fields = ['user', 'created_at']  # User is set automatically based on the logged-in user

from rest_framework import serializers
from .models import CustomUser, Tour, Review, Booking

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser, Tour, Review, Booking
from .serializers import CustomUserSerializer, TourSerializer, ReviewSerializer, BookingSerializer

class AllModelsView(APIView):
    def get(self, request):
        # Fetch all data from each model
        users = CustomUser.objects.all()
        tours = Tour.objects.all()
        reviews = Review.objects.all()
        bookings = Booking.objects.all()

        # Serialize the data
        users_data = CustomUserSerializer(users, many=True).data
        tours_data = TourSerializer(tours, many=True).data
        reviews_data = ReviewSerializer(reviews, many=True).data
        bookings_data = BookingSerializer(bookings, many=True).data

        # Return all data as a single JSON response
        return Response({
            "users": users_data,
            "tours": tours_data,
            "reviews": reviews_data,
            "bookings": bookings_data
        })
