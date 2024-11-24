from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TourViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'tours', TourViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path
from .views import AllModelsView

urlpatterns = [
    path('all-data/', AllModelsView.as_view(), name='all-data'),
]