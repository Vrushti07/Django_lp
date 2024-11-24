from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .models import Tour, Review
from .serializers import TourSerializer, ReviewSerializer
from .permissions import IsTourGuideOrReadOnly, CanReviewBookedTour, IsOwnerOrReadOnly

class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    permission_classes = [IsAuthenticated, IsTourGuideOrReadOnly]

from rest_framework.exceptions import PermissionDenied

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can leave reviews

    def perform_create(self, serializer):
        """
        Set the user automatically to the logged-in user
        when creating a review.
        """
        serializer.save(user=self.request.user)

    def get_queryset(self):
        """
        Restrict reviews to only those of the logged-in user
        for write permissions or allow reading all reviews.
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            return self.queryset.filter(user=self.request.user)
        return self.queryset

    def destroy(self, request, *args, **kwargs):
        """
        Only allow the review owner to delete their own reviews.
        """
        review = self.get_object()
        if review.user != request.user:
            raise PermissionDenied("You can only delete your own reviews.")
        return super().destroy(request, *args, **kwargs)

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Tour
from .serializers import TourSerializer
from .filters import TourFilter

class TourViewSet(viewsets.ModelViewSet):
    queryset = Tour.objects.all()
    serializer_class = TourSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TourFilter


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
