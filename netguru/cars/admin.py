from django.contrib.admin import ModelAdmin, register

from netguru.cars.models import Car, Make, Rating


@register(Car)
class CarAdmin(ModelAdmin):
    fields = (
        'make',
        'model',
    )


@register(Make)
class MakeAdmin(ModelAdmin):
    fields = (
        'name',
        'vpic_id',
    )


@register(Rating)
class RatingAdmin(ModelAdmin):
    fields = (
        'car',
        'rate',
    )
