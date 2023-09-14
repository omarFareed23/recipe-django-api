"""
Models Testing
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core import models


class TestModel(TestCase):
    """"Test models"""

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'pass1234'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        sample_emails = [
            ['test1@example.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['Test3@EXAMPLE.com', 'Test3@example.com']
        ]
        for email, expected_email in sample_emails:
            user = get_user_model().objects.create_user(email, 'test1234')
            self.assertEqual(user.email, expected_email)

    def test_new_user_without_email_raises_error(self):
        """Test creating user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test1234')

    def test_new_user_with_invalid_email_raises_error(self):
        wrong_emails = ['test', 'test@', 'test@e', '']
        for wrong_email in wrong_emails:
            with self.assertRaises(ValueError):
                get_user_model().objects.create_user(wrong_email, 'test1234')
        valid_emails = ['ex1@e.com', 'ex2@fjs.com']
        for valid_email in valid_emails:
            try:
                get_user_model().objects.create_user(valid_email, 'test1234')
            except ValueError:
                self.fail(f'Unexpected ValueError for {valid_email}')

    def test_create_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test1234'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_reciepe(self):
        """Test creating a new recipe"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'pass1234'
        )
        recipe = models.Recipe.objects.create(
            user=user,
            title='Pancake',
            time_minutes=30,
            price=Decimal('5.00'),
            description='Delicious pancakes'
        )
        self.assertEqual(recipe.user, user)
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a new tag"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'pass1234'
        )
        tag = models.Tags.objects.create(
            user=user,
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)
