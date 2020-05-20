from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.test import TestCase
from core.models import Ingredient
from django.urls import reverse
from recipe.serializers import IngredientSerializer

INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientApiTest(TestCase):
    """test for the public api access"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """ test whether the data is accessible without login"""
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):
    """ test for the private api access """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test1@gmail.com',
            'test@123'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredient_list(self):
        """ test retrieving a list of ingredient"""
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Salt')
        res = self.client.get(INGREDIENT_URL)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """test that only ingredients for authentcated user is retrieved"""
        user2 = get_user_model().objects.create_user(
            'test223@gmail.com',
            'test23@222'
        )
        Ingredient.objects.create(user=user2, name='Vinegar')
        ingredients = Ingredient.objects.create(user=self.user, name='Tumeric')

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredients.name)

    def test_create_ingredient_successful(self):
        """ test to check the ingredient creation"""
        payload = {'name': 'Cabbage'}
        self.client.post(INGREDIENT_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name'],
        ).exists()

        self.assertTrue(exists)

    def test_invalid_ingredient_created(self):
        """test to check if invalid payload is accepted"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
