from django.test import Client, RequestFactory, TestCase


class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get("/", HTTP_HOST="outis.com")
        self.assertEqual(response.status_code, 400)
        response = self.c.get("/", HTTP_HOST="clavem.co")
        self.assertEqual(response.status_code, 200)
