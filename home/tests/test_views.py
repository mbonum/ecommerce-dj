from django.test import TestCase
from django.urls import reverse
from django.test import Client

class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()

    def test_url_allowed_hosts(self):
        response = self.c.get("/")
        self.assertEqual(response.status_code, 200)

    # def test_reverse_url(self):
    #     response = self.c.get(reverse)

