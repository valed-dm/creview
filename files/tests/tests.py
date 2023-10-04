from django.contrib.auth import get_user_model
from django.test import TestCase
from files.models import File


class FileTestCase(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user(
            username='test',
            email='test@example.com',
            password='passwordtest'
        )
