from django.urls import path
from . import views

app_name = 'korpa'

urlpatterns = [
    path('', views.korpa_detaljno, name='korpa_detaljno'),
    path('dodaj/<int:proizvod_id>/', views.korpa_dodaj, name='korpa_dodaj'),
    path('ukloni/<int:proizvod_id>/',
         views.korpa_ukloni,
         name='korpa_ukloni'),
]
