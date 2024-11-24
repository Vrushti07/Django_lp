from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsTourGuide(BasePermission):
    """
    Allows access only to tour guides for create, update, and delete actions.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'tour_guide'

class IsTourGuideOrReadOnly(BasePermission):
    """
    Allows tour guides to create, update, and delete tours.
    Regular users can only view.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'tour_guide'

class CanReviewBookedTour(BasePermission):
    """
    Allows only users who have booked a tour to review it.
    """
    def has_permission(self, request, view):
        # Only users with 'user' role can review a tour, and only if they booked it
        if request.user.is_authenticated and request.user.role == 'user' and view.action == 'create':
            # Check if the user has booked this tour (pseudo-code, adjust to match your actual booking logic)
            tour_id = request.data.get('tour_id')
            return request.user.bookings.filter(tour_id=tour_id).exists()
        return False

class IsOwnerOrReadOnly(BasePermission):
    """
    Allows users to edit/delete their own reviews only.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
    
    
