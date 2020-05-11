from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@outlook.com",
            password="Admin@123"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="test@gmail.com",
            password="test@123",
            name="Test username"
        )

    def test_user_listed(self):
        """test whether the user is listed on user page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """test whether the user page is editable"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEquals(res.status_code, 200)

    def test_user_creation(self):
        """test whether the new user can be created"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEquals(res.status_code, 200)
