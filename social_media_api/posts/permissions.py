from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit or delete it.
    Read permissions are allowed to any authenticated user.
    """
    def has_permission(self, request, view):
        """
        Check if user is authentiated for any request
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Read permissions are allowed to any authenticated user
        Write permissions are only allowed to the author of the object.
        """
        #Read permissions are allowed to any authenticated user
        #Always allow GET, HEAD, OPTIONS request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        #Write permissions are only allowed to the author of the post or comment
        return obj.author == request.user