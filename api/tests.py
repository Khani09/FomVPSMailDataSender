from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

API_KEY = "your-secure-api-key"
HEADERS = {"HTTP_X_API_KEY": API_KEY}

class MailMonitorAPITests(APITestCase):
    def test_logs_endpoint(self):
        url = reverse("mail-logs")
        response = self.client.get(url, **HEADERS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_received_endpoint(self):
        url = reverse("received-mails")
        response = self.client.get(url, **HEADERS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_outgoing_endpoint(self):
        url = reverse("outgoing-mails")
        response = self.client.get(url, **HEADERS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_status_endpoint(self):
        url = reverse("postfix-status")
        response = self.client.get(url, **HEADERS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_errors_endpoint(self):
        url = reverse("mail-errors")
        response = self.client.get(url, **HEADERS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_queue_endpoint(self):
        url = reverse("mail-queue")
        response = self.client.get(url, **HEADERS)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
