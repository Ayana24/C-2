from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User, PerevalAdded

class PerevalAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@example.com", fam="Иванов", name="Иван", otc="Иванович", phone="1234567890")
        self.pereval_data = {
            "user": {
                "email": "test@example.com",
                "fam": "Иванов",
                "name": "Иван",
                "otc": "Иванович",
                "phone": "1234567890"
            },
            "coords": {
                "latitude": 45.0,
                "longitude": 90.0,
                "height": 1000
            },
            "beauty_title": "пер.",
            "title": "Тестовый перевал",
            "other_titles": "Альтернативное название",
            "level": {
                "winter": "1A",
                "summer": "1B",
                "autumn": "1A",
                "spring": "1B"
            },
            "images": [
                {"data": "base64_string", "title": "Вид с вершины"}
            ]
        }

    def test_create_pereval(self):
        url = reverse('pereval-list')
        response = self.client.post(url, self.pereval_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_perevals(self):
        url = reverse('pereval-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
