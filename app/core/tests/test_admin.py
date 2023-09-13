"""
Tests for Django admin
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    """Tests for django admin"""

    # add a setUp function to run before every test
    def setUp(self):
        """Setting up the test"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='pass1234'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='pass1234',
            name='Test User'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        # generate url for list user page
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        # assertContains checks if response contains certain item
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)
