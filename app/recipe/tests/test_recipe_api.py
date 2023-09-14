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
from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


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


def get_recipe_detail_url(recipe_id):
    """Return recipe detail url"""
    return reverse('recipe:recipe-detail', args=[recipe_id])


class PublicRecipeApiTest(TestCase):
    """Test the recipe API (public)"""

    def setUp(self):
        """Setting up the test"""
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_recipe_invalid(self):
        """Test creating a new recipe needs authentication"""
        user = get_user_model().objects.create_user(
            'test3@exam.com',
            'pass1234'
        )
        payload = {
            'title': 'Test Recipe',
            'time_minutes': 10,
            'price': Decimal('5.00'),
            'description': 'Test Recipe Description',
            'link': 'http://test.com',
            'user': user.id
        }
        res = self.client.post(RECIPE_URL, payload.copy())
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

    def test_get_recipe_detail(self):
        """Test getting recipe detail"""
        recipe = create_recipe(user=self.user)
        url = get_recipe_detail_url(recipe.id)
        res = self.client.get(url)
        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_receipe(self):
        """Test creating a new recipe"""
        payload = {
            'title': 'Test Recipe',
            'time_minutes': 10,
            'price': Decimal('5.00'),
            'description': 'Test Recipe Description',
            'link': 'http://test.com',
        }
        res = self.client.post(RECIPE_URL, payload)
        # import pdb; pdb.set_trace()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)
        self.assertEqual(recipe.user, self.user)

    def test_update_recipe(self):
        """Test updating a recipe"""
        recipe = create_recipe(user=self.user)
        payload = {
            'title': 'Updated Title',
            'time_minutes': 20,
            'price': Decimal('10.00'),
            'description': 'Updated Description',
            'link': 'http://updated.com',
        }
        url = get_recipe_detail_url(recipe.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)

    def test_update_reciepe(self):
        """Test updating a recipe for only the owner"""
        recipe = create_recipe(user=self.user)
        payload = {
            'title': 'Updated Title',
            'time_minutes': 20,
            'price': Decimal('10.00'),
            'description': 'Updated Description',
            'link': 'http://updated.com',
        }
        url = get_recipe_detail_url(recipe.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        recipe.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(recipe, k), v)

    def test_update_for_only_the_owner(self):
        """Test updating a recipe for only the owner"""
        # import pdb; pdb.set_trace()
        user2 = get_user_model().objects.create_user(
            'test2@exampl.com',
            'pass1234'
        )
        recipe = create_recipe(user=user2)
        payload = {
            'title': 'Updated Title',
            'time_minutes': 20,
            'price': Decimal('10.00'),
            'description': 'Updated Description',
            'link': 'http://updated.com',
        }
        url = get_recipe_detail_url(recipe.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_reciepe(self):
        """Test deleting a recipe"""
        recipe = create_recipe(user=self.user)
        url = get_recipe_detail_url(recipe.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
