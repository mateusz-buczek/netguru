from django.urls import path
from rest_framework import routers

from cars.api.cars.views import CarView, RatingView, PopularView

app_name = 'api'
urlpatterns = [
    path(r'rate', RatingView.as_view(), name='rate'),
    path(r'popular', PopularView.as_view(), name='popular'),
]

router = routers.SimpleRouter()

router.register(r'cars', CarView, basename='cars')

urlpatterns += router.urls
