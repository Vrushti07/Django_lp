# filters.py

from django_filters import rest_framework as filters
from .models import Tour
from datetime import date

class TourFilter(filters.FilterSet):
    # Price filter (ascending and descending)
    price = filters.OrderingFilter(fields=['price'], label='Price')
    
    # Ratings filter
    ratings = filters.OrderingFilter(fields=['average_rating'], label='Ratings')

    # Duration filter
    duration = filters.OrderingFilter(fields=['no_of_days'], label='Duration')

    # Datewise filter: filter out tours that have a past date
    future_tours = filters.BooleanFilter(method='filter_future_tours', label='Upcoming Only')

    # Type filter: filter for specific age groups or family-friendly tours
    age_group = filters.CharFilter(field_name='age_group', lookup_expr='iexact')
    family_friendly = filters.BooleanFilter(field_name='is_family_friendly')

    class Meta:
        model = Tour
        fields = ['price', 'ratings', 'duration', 'future_tours', 'age_group', 'family_friendly']

    def filter_future_tours(self, queryset, name, value):
        if value:
            return queryset.filter(date__gte=date.today())
        return queryset
