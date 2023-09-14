"""
Views for recipe app
"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer, TagSerializer


class RecipeView(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    serializer_class = RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-id').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return RecipeSerializer
        return self.serializer_class

    # this function is called every time you create an object
    # Inside the create method, the perform_create method is called.
    def perform_create(self, serializer):
        """Create a new recipe"""
        # set the user to the authenticated user
        serializer.save(user=self.request.user)


class TagView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """Manage tags in the database"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')
