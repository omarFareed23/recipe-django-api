"""
User API Tests
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse('user:create')
TEST_USER_DETAILS = {
    'email': 'test@example.com',
    'password': 'testpass',
    'name': 'Test User'
}
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        """Setting up the test"""
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = TEST_USER_DETAILS.copy()
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        # check if password is correct
        self.assertTrue(user.check_password(payload['password']))
        # check if password is not in respo nse
        self.assertNotIn('password', res.data)

    def test_user_with_exists_email_throw_error(self):
        """Test creating user with email already exists"""
        payload = TEST_USER_DETAILS.copy()
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 8 characters"""
        payload = TEST_USER_DETAILS.copy()
        payload['password'] = 'pw'
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        create_user(**TEST_USER_DETAILS)
        payload = TEST_USER_DETAILS.copy()
        payload.pop('name')
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(**TEST_USER_DETAILS)
        payload = TEST_USER_DETAILS.copy()
        payload['password'] = 'wrongpass'
        payload.pop('name')
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrive_user_unauthorized(self):
        """Test that authentication is required for users"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTest(TestCase):
    """Test API requests that require authentication"""

    def setUp(self):
        """Setting up the test"""
        self.user = create_user(**TEST_USER_DETAILS)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email
        })

    def test_post_method_not_allowed(self):
        """Test that POST is not allowed on the me URL"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating user profile for authenticated user"""
        payload = {'name': 'Other Name', 'password': 'otherPass'}
        # import pdb; pdb.set_trace()
        _ = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
