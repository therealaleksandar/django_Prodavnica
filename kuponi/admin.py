from django.contrib import admin
from .models import Kupon


@admin.register(Kupon)
class KuponAdmin(admin.ModelAdmin):
    list_display = ['kod', 'aktivno', 'popust', 'vazi_od', 'vazi_do']
    list_filter = ['aktivno', 'vazi_od', 'vazi_do']
    search_fields = ['kod']
