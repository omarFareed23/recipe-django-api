"""
User API Tests
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class PublicUserApiTest(TestCase):
    """Test the users API (public)"""

    __create_user_url = reverse('user:create')
    __test_user_payload = {
        'email': 'test@example.com',
        'password': 'testpass',
        'name': 'Test User'
    }
    __token_url = reverse('user:token')

    def __create_user(self, **params):
        """Helper function to create new user"""
        return get_user_model().objects.create_user(**params)

    def setUp(self):
        """Setting up the test"""
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful"""
        payload = self.__test_user_payload.copy()
        res = self.client.post(self.__create_user_url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        # check if password is correct
        self.assertTrue(user.check_password(payload['password']))
        # check if password is not in respo nse
        self.assertNotIn('password', res.data)

    def test_user_with_exists_email_throw_error(self):
        """Test creating user with email already exists"""
        payload = self.__test_user_payload.copy()
        self.__create_user(**payload)
        res = self.client.post(self.__create_user_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 8 characters"""
        payload = self.__test_user_payload.copy()
        payload['password'] = 'pw'
        res = self.client.post(self.__create_user_url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        self.__create_user(**self.__test_user_payload)
        payload = self.__test_user_payload.copy()
        payload.pop('name')
        res = self.client.post(self.__token_url, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        self.__create_user(**self.__test_user_payload)
        payload = self.__test_user_payload.copy()
        payload['password'] = 'wrongpass'
        payload.pop('name')
        res = self.client.post(self.__token_url, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
