from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APITestCase

from netguru.cars.models import Car, Make, Rating


class RatingsTests(APITestCase):
    def setUp(self):
        self.url = reverse('api:rate')
        self.make_1 = mixer.blend(Make)
        self.car_1 = mixer.blend(Car, make=self.make_1)

    def test_post_rate_with_no_data(self):
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_rate_with_no_car_id(self):
        data = {'rate': 5}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_rate_with_no_rate(self):
        data = {'car': self.car_1.id}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_rate_with_invalid_car_id(self):
        data = {'car': 0, 'rate': 5}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_rate_with_rate_below_range(self):
        data = {'car': self.car_1.id, 'rate': 0}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_rate_with_rate_above_range(self):
        data = {'car': self.car_1.id, 'rate': 6}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_rate_with_valid_data(self):
        data = {'car': self.car_1.id, 'rate': 5}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.all().count(), 1)
