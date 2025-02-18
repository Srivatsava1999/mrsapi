from rest_framework.permissions import BasePermission
from Users.models import UserAccount

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role==UserAccount.ADMIN

class IsEnterpriseUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role==UserAccount.ENTERPRISE

class IsCustomerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role==UserAccount.CUSTOMER
