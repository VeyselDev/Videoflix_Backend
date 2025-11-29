from django.test import TestCase

from app_authentication.models import CustomUser


class TestCustomUserModel(TestCase):

    def test_create_superuser(self):
        email = 'admin@example.com'
        password = 'password'
        superuser = CustomUser.objects.create_superuser(email=email, password=password)

        self.assertEqual(superuser.email, email)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.check_password(password))
