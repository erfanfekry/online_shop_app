from rest_framework.permissions import BasePermission

class IsAdminKhorasani(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_superuser and user.phone.startswith('0915')


class IsBuyer(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.buyer == request.user