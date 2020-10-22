from django.urls import reverse
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APITestCase

from netguru.cars.models import Car, Make, Rating


class CarCreateTests(APITestCase):
    def test_create_new_car_with_valid_data(self):
        self.assertEqual(Car.objects.all().count(), 0)
        url = reverse('api:cars-list')
        data = {'make': 'honda', 'model': 'civic'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['message'], "Successfully found and saved")
        self.assertEqual(Car.objects.all().count(), 1)
        self.assertEqual(Car.objects.first().model, 'Civic')
        self.assertEqual(str(Car.objects.first().make), 'HONDA')

    def test_create_without_make_data(self):
        self.assertEqual(Car.objects.all().count(), 0)
        url = reverse('api:cars-list')
        data = {'model': 'civic'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], "Make not specified")
        self.assertEqual(Car.objects.all().count(), 0)

    def test_create_without_model_data(self):
        self.assertEqual(Car.objects.all().count(), 0)
        url = reverse('api:cars-list')
        data = {'make': 'civic'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], "Model not specified")
        self.assertEqual(Car.objects.all().count(), 0)

    def test_create_returning_multiple_results(self):
        self.assertEqual(Car.objects.all().count(), 0)
        url = reverse('api:cars-list')
        data = {'make': 'b', 'model': '0'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['message'], "More than one result returned, please specify your search")
        self.assertEqual(Car.objects.all().count(), 0)

    def test_create_returning_no_results(self):
        self.assertEqual(Car.objects.all().count(), 0)
        url = reverse('api:cars-list')
        data = {'make': 'bghdfgfhd', 'model': '0'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['error'], "Car with these parameters does not exist")
        self.assertEqual(Car.objects.all().count(), 0)

    def test_create_same_car_twice(self):
        self.assertEqual(Car.objects.all().count(), 0)
        url = reverse('api:cars-list')
        data = {'make': 'honda', 'model': 'civic'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['message'], "Successfully found and saved")
        self.assertEqual(Car.objects.all().count(), 1)
        response_clone = self.client.post(url, data, format='json')
        self.assertEqual(response_clone.status_code, status.HTTP_200_OK)
        self.assertEqual(response_clone.json()['message'], "Already in database")
        self.assertEqual(Car.objects.all().count(), 1)


class CarListTests(APITestCase):
    def setUp(self):
        self.url = reverse('api:cars-list')
        self.make_1 = mixer.blend(Make)

    def test_no_cars_in_db(self):
        self.assertEqual(Car.objects.all().count(), 0)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.json()), 0)

    def test_one_car_in_db(self):
        self.assertEqual(Car.objects.all().count(), 0)
        car_1 = mixer.blend(Car, make=self.make_1)
        self.assertEqual(Car.objects.all().count(), 1)
        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.json()), 1)

    def test_average_rating(self):
        self.assertEqual(Car.objects.all().count(), 0)
        car_1 = mixer.blend(Car, make=self.make_1)
        rating_1 = mixer.blend(Rating, car=car_1)
        rating_2 = mixer.blend(Rating, car=car_1)
        self.assertEqual(Rating.objects.filter(car=car_1).count(), 2)

        avg = (rating_1.rate + rating_2.rate) / Rating.objects.filter(car=car_1).count()

        response = self.client.get(self.url, format='json')
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]['average_rating'], avg)
