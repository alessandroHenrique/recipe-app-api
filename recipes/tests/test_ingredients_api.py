from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core import models
from recipes import serializers


INGREDIENTS_URL = reverse('recipes:ingredient-list')


class PublicIngridientApiTests(TestCase):
    """Test the publicly available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test the private ingredients API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            name='test',
            email='test@gmail.com',
            password='pass2323'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """Test retrieving a list of ingredients"""
        models.Ingredient.objects.create(user=self.user, name='Kale')
        models.Ingredient.objects.create(user=self.user, name='Salt')

        response = self.client.get(INGREDIENTS_URL)
        ingredients = models.Ingredient.objects.all().order_by('-name')
        serializer = serializers.IngredientSerializer(ingredients, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """Test that ingredients for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            email="another@gmail.com",
            password="anotherpass",
            name="another"
        )
        models.Ingredient.objects.create(user=user2, name='Vinegar')

        ingredient = models.Ingredient.objects.create(user=self.user,
                                                      name='Tumeric')
        response = self.client.get(INGREDIENTS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], ingredient.name)
