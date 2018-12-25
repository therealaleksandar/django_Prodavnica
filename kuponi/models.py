from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Kupon(models.Model):
    kod = models.CharField(max_length=50, unique=True)
    vazi_od = models.DateTimeField()
    vazi_do = models.DateTimeField()
    aktivno = models.BooleanField(default=True)
    popust = models.IntegerField(validators=[
                                 MaxValueValidator(100), MinValueValidator(0)])

    class Meta:
        verbose_name_plural = 'Kuponi'

    def __str__(self):
        return self.kod
