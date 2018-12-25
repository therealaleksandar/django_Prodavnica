from django.urls import path
from . import views

app_name = 'prodavnica'

urlpatterns = [
    path('', views.proizvodi_lista, name='proizvodi_lista'),
    path('<slug:kategorija_slug>/',
         views.proizvodi_lista,
         name='proizvodi_lista_kategorija'),
    path('<int:id>/<slug:proizvod_slug>/',
         views.proizvod_detaljno,
         name='proizvod_detaljno'),
]
