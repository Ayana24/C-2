from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import PerevalAdded, Coord, User


class SubmitDataTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.valid_payload = {
            "user": {
                "email": "ivan@example.com",
                "fam": "Иванов",
                "name": "Иван",
                "otc": "Иванович",
                "phone": "89991112233"
            },
            "coords": {
                "latitude": 45.123,
                "longitude": 37.456,
                "height": 1200
            },
            "beauty_title": "пер.",
            "title": "Ай-Юлю",
            "other_titles": "Аюлю",
            "connect": "",
            "level_winter": "1A",
            "level_summer": "1B",
            "level_autumn": "1A",
            "level_spring": "1A",
            "images": []
        }

    def test_create_pereval(self):
        """Тест создания перевала"""
        response = self.client.post(reverse('submit-data'), self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PerevalAdded.objects.exists())

    def test_get_pereval(self):
        """Тест получения созданного перевала"""
        response = self.client.post(reverse('submit-data'), self.valid_payload, format='json')
        pereval_id = response.data['id']
        response = self.client.get(reverse('get-pereval', kwargs={'pk': pereval_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Ай-Юлю")

    def test_patch_reject_update_on_moderated(self):
        """Тест запрета обновления записи, не находящейся в статусе 'new'"""
        response = self.client.post(reverse('submit-data'), self.valid_payload, format='json')
        pereval_id = response.data['id']
        pereval = PerevalAdded.objects.get(id=pereval_id)
        pereval.status = 'accepted'
        pereval.save()

        patch_payload = self.valid_payload.copy()
        patch_payload['title'] = 'Новое название'

        response = self.client.patch(reverse('update-pereval', kwargs={'pk': pereval_id}), patch_payload, format='json')
        self.assertEqual(response.data['state'], 0)
        self.assertIn("нельзя редактировать", response.data['message'])

    def test_filter_by_email(self):
        """Тест фильтрации по email"""
        self.client.post(reverse('submit-data'), self.valid_payload, format='json')
        response = self.client.get(reverse('filter-perevals'), {'user__email': 'ivan@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
