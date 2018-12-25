from django.urls import path
from . import views
from django.utils.text import gettext_lazy as _

app_name = 'narudzbina'

urlpatterns = [
    path(_('kreiraj/'), views.narudzbina_dodaj, name='narudzbina_dodaj'),
    path('admin/narudzbina/<int:narudzbina_id>/', views.admin_narudzbina_detaljno,
         name='admin_narudzbina_detaljno'),
    path('admin/narudzbina/pdf/<int:narudzbina_id>/', views.admin_narudzbina_pdf,
         name='admin_narudzbina_pdf')
]
