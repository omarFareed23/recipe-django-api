from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag
from tag.serializers import TagSerializer


def create_tag(user, name=None):
    """Helper function to create new tag"""
    if name is None:
        name = 'Sample Tag'
    return Tag.objects.create(user=user, name=name)


TAGS_URL = reverse('recipe:tag-list')


class PublicTagTesting(TestCase):
    """Test the publicly available tag API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagTesting(TestCase):
    """Test the authorized user tag API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@example.com'
            'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        create_tag(self.user)
        create_tag(self.user, 'Test Tag')
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.data, serializer.data)
