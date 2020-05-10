from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_address(self):
        """test the user entered username and email address"""
        email = "test@gmail.com"
        password = "Testpass123"

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_user_email_with_normalize(self):
        """test the email address is normalized """
        email = "test@GMAIL.COM"

        user = get_user_model().objects.create_user(
            email=email,
            password="test123"
        )

        self.assertEqual(user.email, email.lower())

    def test_user_email_address_validation(self):
        """test whether user entered a valid email address"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "hsjdf")

    def test_is_the_user_superuser(self):
        """ test whether a superuser can be created """
        email = "admin@gmail.com"
        user = get_user_model().objects.create_superuser(
            email=email,
            password="super#user"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
