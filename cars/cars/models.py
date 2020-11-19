from django.db import models


class Car(models.Model):
    make = models.ForeignKey(
        'Make',
        related_name='cars',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    model = models.CharField(max_length=250)

    def __str__(self):
        return f'{self.make.name} {self.model}'


class Make(models.Model):
    name = models.CharField(max_length=250)
    vpic_id = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.name)


class Rating(models.Model):
    RATE_CHOICES = list([(x, str(x)) for x in range(1, 6)])
    car = models.ForeignKey(
        'Car',
        related_name='ratings',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    rate = models.IntegerField(choices=RATE_CHOICES)

    def __str__(self):
        return f'{str(self.car)} - {self.rate}'
