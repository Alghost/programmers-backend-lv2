from django.test import TestCase
from django.contrib.auth.hashers import check_password
from .models import Fbuser

# Create your tests here.


class YourTestClass(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        self.user = Fbuser(
            username='testuser',
            password='dlxoghk1!A',
            email='testuser@gmail.com',
            is_active=True,
            is_staff=True
        )
        self.user.save()

        print(self.user.password)

    def test_password(self):
        pass
