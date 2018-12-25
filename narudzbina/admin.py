import csv
import datetime
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.http import HttpResponse
from django.contrib import admin
from .models import Narudzbina, NarudzbinaPredmet


def narudzbina_pdf(obj):
    return mark_safe('<a href="{}">PDF</a>'.format(
        reverse('narudzbina:admin_narudzbina_pdf', args=[obj.id])))


def narudzbina_detaljno(obj):
    return mark_safe('<a href="{}">Pogledaj</a>'.format(
        reverse('narudzbina:admin_narudzbina_detaljno', args=[obj.id])))


class NarudzbinaPredmetInline(admin.TabularInline):
    model = NarudzbinaPredmet
    raw_id_fields = ['proizvod']


@admin.register(Narudzbina)
class NarudzbinaAdmin(admin.ModelAdmin):
    list_display = ['id', 'ime', 'prezime', 'email', 'adresa',
                    'postanski_broj', 'mesto', 'placeno',
                    'kreirano', 'azurirano', narudzbina_pdf, narudzbina_detaljno]
    list_filter = ['placeno', 'kreirano', 'azurirano']
    inlines = [NarudzbinaPredmetInline]
    actions = ['export_to_csv']

    def export_to_csv(self, request, queryset):
        opts = self.model._meta
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="{}.csv'.format(
            opts.verbose_name)
        writer = csv.writer(response)
        polja = [
            polje for polje in opts.get_fields()
            if not polje.many_to_many and not polje.one_to_many]
        writer.writerow([polje.verbose_name for polje in polja])
        for obj in queryset:
            red_podataka = []
            for polje in polja:
                value = getattr(obj, polje.name)
                if isinstance(value, datetime.datetime):
                    value = value.strftime('%d/%m/%Y')
                red_podataka.append(value)
            writer.writerow(red_podataka)
        return response
    export_to_csv.short_description = 'Eksportuj u CSV'
