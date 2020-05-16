from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag
from recipe.serializers import TagSerializer

TAGS_URL = reverse("recipe:tag-list")


class PublicTagApiTest(TestCase):
    """ test the publicly available tag api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required to access the tags"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTest(TestCase):
    """Test the private tag api"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'test@123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_recieve_tags(self):
        """test recieve tags"""
        Tag.objects.create(user=self.user, name="Vegan")
        Tag.objects.create(user=self.user, name="Dessert")

        res = self.client.get(TAGS_URL)
        tags = Tag.objects.all().order_by("-name")
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """test that tags returned are for the authorised user"""
        user2 = get_user_model().objects.create_user(
            'test2@gmail.com',
            'test2@123'
        )
        Tag.objects.create(user=user2, name="Fruity")
        tag = Tag.objects.create(user=self.user, name="Comfort food")

        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
