from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields


class Kategorija(TranslatableModel):
    translations = TranslatedFields(
        ime=models.CharField(max_length=25, db_index=True),
        slug=models.SlugField(unique=True, max_length=25)
    )

    class Meta:
        # ordering = ('ime',)
        verbose_name = 'kategorija'
        verbose_name_plural = 'kategorije'

    def __str__(self):
        return self.ime

    def get_absolute_url(self):
        return reverse('prodavnica:proizvodi_lista_kategorija',
                       args=[self.slug])


class Proizvod(TranslatableModel):
    translations = TranslatedFields(
        ime=models.CharField(db_index=True, max_length=200),
        opis=models.TextField(),
        slug=models.SlugField(db_index=True, max_length=200, unique=True)
    )
    slika = models.ImageField(upload_to='proizvodi/%Y/%m/%d',
                              blank=True,
                              default='proizvodi/no_image.png')
    cena = models.DecimalField(max_digits=10, decimal_places=2)
    kreirano = models.DateTimeField(auto_now_add=True)
    azurirano = models.DateTimeField(auto_now=True)
    kategorija = models.ForeignKey(Kategorija,
                                   related_name='proizvodi',
                                   on_delete=models.CASCADE)
    dostupno = models.BooleanField(default=True)

    class Meta:
        #     ordering = ('-kreirano',)
        #     index_together = (('id', 'slug'),)
        verbose_name_plural = 'proizvodi'

    def __str__(self):
        return self.ime

    def get_absolute_url(self):
        return reverse('prodavnica:proizvod_detaljno',
                       args=[self.id, self.slug])
