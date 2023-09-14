"""
Tag views
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Tag
from tag.serializers import TagSerializer


class TagViewSets(viewsets.ModelViewSet):
    """Manage tags in the database"""
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).order_by('-name')
