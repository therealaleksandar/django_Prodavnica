from django.db import models
from decimal import Decimal
from django.core.validators import MaxValueValidator, MinValueValidator
from kuponi.models import Kupon
from prodavnica.models import Proizvod
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import gettext_lazy as _


class Narudzbina(models.Model):
    ime = models.CharField(_('ime'), max_length=50)
    prezime = models.CharField(_('prezime'), max_length=50)
    email = models.EmailField(_('email'),)
    adresa = models.CharField(_('adresa'), max_length=250)
    postanski_broj = models.PositiveIntegerField(_('postanski broj'),
                                                 validators=[MaxValueValidator(99999),
                                                             MinValueValidator(10000)])
    mesto = models.CharField(_('mesto'), max_length=100)
    kreirano = models.DateTimeField(auto_now_add=True)
    azurirano = models.DateTimeField(auto_now=True)
    placeno = models.BooleanField(default=False)
    braintree_id = models.CharField(blank=True, max_length=150)
    kupon = models.ForeignKey(Kupon,
                              on_delete=models.SET_NULL,
                              related_name='narudzbine',
                              null=True,
                              blank=True)
    popust = models.IntegerField(default=0,
                                 validators=[MaxValueValidator(100),
                                             MinValueValidator(0)])

    class Meta:
        ordering = ('-kreirano',)
        verbose_name_plural = 'narudzbine'

    def __str__(self):
        return 'Narudzbina {}'.format(self.id)

    def dobij_punu_cenu(self):
        return sum(predmet.dobij_cenu() for predmet in self.predmeti.all())

    def dobij_popust(self):
        return self.dobij_punu_cenu()*(self.popust/Decimal('100'))

    def dobij_punu_cenu_posle_popusta(self):
        return self.dobij_punu_cenu()-self.dobij_popust()


class NarudzbinaPredmet(models.Model):
    narudzbina = models.ForeignKey(
        Narudzbina, related_name='predmeti', on_delete=models.CASCADE)
    proizvod = models.ForeignKey(
        Proizvod, related_name='narudzbina_predmeti', on_delete=models.CASCADE)
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    kolicina = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def dobij_cenu(self):
        return self.cena*self.kolicina
