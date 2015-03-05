from rest_framework import permissions
from django.contrib.auth.models import User
from gps.models import GpsNode, GpsNodeMetrics
import pdb

class IsAuthenticatedAndOwned(permissions.IsAuthenticatedOrReadOnly):
    def has_object_permission(self, request, view, obj):
        res=super(IsAuthenticatedAndOwned, self).has_object_permission(request, view, obj)
        if res: # Is Authenticated
            # also check object owner to be itself.
            if request.user.is_staff:
                return True
            elif isinstance(obj, User):
                if obj.id == request.user.id:
                    return True 
            elif isinstance(obj, GpsNode):
                if obj.user.id == request.user.id:
                    return True 
            elif isinstance(obj, GpsNodeMetrics):
                if obj.node.user.id == request.user.id:
                    return True
        return False

class IsOwnerOrNone(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        #pdb.set_trace()
        if request.user.is_superuser or request.user.is_staff:
            return True

        # Any other permissions are only allowed to the owner.
        return obj.user == request.user

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        #pdb.set_trace()
        print "has_object_permission(self=%r, req=%r, view=%r,obj=%r" % (self, request, view, obj)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user.id  == request.user.id
