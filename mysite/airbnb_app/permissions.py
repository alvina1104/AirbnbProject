from rest_framework.permissions import BasePermission


class CheckRolePermission(BasePermission):
    def has_permission(self,request,view):
        return request.user.user_role == 'guest'


class CreatePropertyPermission(BasePermission):
    def has_permission(self,request,view):
        return request.user.user_role == 'owner'


class CreatePropertyHostPermission(BasePermission):
    def has_permission(self,request,view):
        return request.user.user_role == 'host'