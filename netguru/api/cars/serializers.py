from rest_framework import serializers

from netguru.cars.models import Car, Make, Rating


class CarSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField(read_only=True)
    make = serializers.SerializerMethodField()

    def get_average_rating(self, obj):
        return obj.average_rating or 'No ratings yet'

    def get_make(self, obj):
        return obj.make.name

    class Meta:
        model = Car
        fields = '__all__'


class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class PopularCarSerializer(serializers.ModelSerializer):
    rates_count = serializers.SerializerMethodField(read_only=True)

    def get_rates_count(self, obj):
        return obj.rates_count

    class Meta:
        model = Car
        fields = '__all__'
