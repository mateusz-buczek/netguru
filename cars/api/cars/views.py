import time

import requests
from django.db.models import Avg, Count
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from cars.api.cars.serializers import CarSerializer, RatingSerializer, PopularCarSerializer
from cars.cars.models import Car, Make


class CarView(ListModelMixin, CreateModelMixin, GenericViewSet):
    """
    View serving:
    - list of all cars already present in application database with their current average rate (on GET, no parameters)
    - creation of new car in database (on POST), required parameters:
        model: car model(case-insensitive)
        make: car make(case-insensitive)
    """
    queryset = Car.objects.all().annotate(
        average_rating=Avg('ratings__rate')
    )
    serializer_class = CarSerializer

    def create(self, request, *args, **kwargs):
        make = str(request.data.get('make', None)).lower()
        model = str(request.data.get('model', None)).lower()
        if make in ["", 'none', None]:
            return Response({"error": "Make not specified"}, status=status.HTTP_400_BAD_REQUEST)
        if model in ["", 'none', None]:
            return Response({"error": "Model not specified"}, status=status.HTTP_400_BAD_REQUEST)

        attempt_num = 0
        while attempt_num < 2:
            try:
                r = requests.get(
                    f"https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{make}?format=json",
                    timeout=1,
                )
            except requests.exceptions.ReadTimeout:
                return Response({"error": "Request failed, timeout exceeded"}, status=status.HTTP_400_BAD_REQUEST)

            if r.status_code == 200:
                data = r.json()
                return_data = []
                for result in data['Results']:
                    if make in result['Make_Name'].lower() and model in result['Model_Name'].lower():
                        return_data.append(result)
                if len(return_data) > 1:
                    return Response(
                        {
                            'message': "More than one result returned, please specify your search",
                            'return_data': return_data,
                        },
                        status=status.HTTP_200_OK
                    )
                elif len(return_data) == 0:
                    return Response(
                        {
                            'error': "Car with these parameters does not exist",
                        },
                        status=status.HTTP_200_OK
                    )
                else:
                    make_data = {
                        'name': return_data[0]['Make_Name'],
                        'vpic_id': return_data[0]['Make_ID'],
                    }
                    make_instance, created = Make.objects.get_or_create(**make_data)
                    car_data = {
                        'make': make_instance,
                        'model': return_data[0]['Model_Name'],
                    }
                    car_instance, created = Car.objects.get_or_create(**car_data)
                    if created:
                        return Response(
                            {
                                'message': "Successfully found and saved",
                                'return_data': return_data,
                            },
                            status=status.HTTP_201_CREATED
                        )
                    else:
                        return Response(
                            {
                                'message': "Already in database",
                                'return_data': return_data,
                            },
                            status=status.HTTP_200_OK
                        )
            else:
                attempt_num += 1
                time.sleep(5)
        return Response(
            {"error": "Request failed, maximum number of attempts reached"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class RatingView(CreateAPIView):
    """
    View allows adding single car rating.
    Can be rated from 1 to 5, requires specifying car ID which can be obtained from Car list view
    """
    serializer_class = RatingSerializer

    def create(self, request, *args, **kwargs):
        car = str(request.data.get('car', None)).lower()
        if car in ["", 'none', None]:
            return Response({"error": "Car not specified"}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)


class PopularView(ListAPIView):
    """
    Shows top cars already present in the database ranking based on number of rates (not average rate values)
    - Important: returns results for cars with at least one rate
    """
    queryset = Car.objects.all().annotate(
        rates_count=Count('ratings')
    ).filter(rates_count__gt=0).order_by('-rates_count')
    serializer_class = PopularCarSerializer
