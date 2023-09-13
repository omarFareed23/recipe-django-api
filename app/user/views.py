"""user API views"""

from rest_framework import generics
from user.serializers import UserSerializer

# generics.CreateAPIView is a generic view that allows you to create an object in a database
# it is a shortcut for creating a view that handles POST requests


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer
