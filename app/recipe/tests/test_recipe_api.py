"""
Tests for recipe api
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe
from recipe.serializers import RecipeSerializer


def create_recipe(user, **params):
    """Helper function to create new recipe"""
    defaults = {
        'title': 'Sample Recipe',
        'time_minutes': 10,
        'price': Decimal('5.00'),
        'description': 'Sample Recipe Description',
        'link': 'http://sample.com',
    }
    defaults.update(params)
    return Recipe.objects.create(user=user, **defaults)


RECIPE_URL = reverse('recipe:recipe-list')


class PublicRecipeApiTest(TestCase):
    """Test the recipe API (public)"""

    def setUp(self):
        """Setting up the test"""
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """Test the recipe API (private)"""

    def setUp(self):
        """Setting up the test"""
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'pass1234'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)
        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # import pdb
        # pdb.set_trace()
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_recipes_limited_to_user(self):
        """Test retrieving recipes for user"""
        user2 = get_user_model().objects.create_user(
            'test2@exampl.com',
            'pass1234'
        )
        create_recipe(user=user2)
        create_recipe(user=self.user)
        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user).order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
