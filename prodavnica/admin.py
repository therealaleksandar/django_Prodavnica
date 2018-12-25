from django.contrib import admin
from .models import Kategorija, Proizvod
from parler.admin import TranslatableAdmin


@admin.register(Kategorija)
class KategorijaAdmin(TranslatableAdmin):
    list_display = ['ime', 'slug']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('ime',)}


@admin.register(Proizvod)
class ProizvodAdmin(TranslatableAdmin):
    list_display = ['ime', 'slug', 'cena', 'dostupno', 'kreirano', 'azurirano']
    list_filter = ['dostupno', 'kreirano', 'azurirano']
    list_editable = ['cena', 'dostupno']

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ['ime']}
