from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APITestCase

from netguru.cars.models import Car, Make, Rating


class PopularTests(APITestCase):
    def setUp(self):
        self.url = reverse('api:popular')
        self.make_1 = mixer.blend(Make)
        self.car_1 = mixer.blend(Car, make=self.make_1)
        self.make_2 = mixer.blend(Make)
        self.car_2 = mixer.blend(Car, make=self.make_2)

    def test_no_rates_in_db(self):
        self.assertEqual(Car.objects.all().count(), 2)
        self.assertEqual(Rating.objects.all().count(), 0)
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 0)

    def test_two_ratings_for_one_car_in_db(self):
        self.assertEqual(Rating.objects.all().count(), 0)
        rating_1 = mixer.blend(Rating, car=self.car_1)
        rating_2 = mixer.blend(Rating, car=self.car_1)
        self.assertEqual(Rating.objects.all().count(), 2)

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_one_rating_for_each_car_in_db(self):
        self.assertEqual(Rating.objects.all().count(), 0)
        rating_1 = mixer.blend(Rating, car=self.car_1)
        rating_2 = mixer.blend(Rating, car=self.car_2)
        self.assertEqual(Rating.objects.all().count(), 2)

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 2)
