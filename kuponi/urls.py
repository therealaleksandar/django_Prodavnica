from django.urls import path
from . import views
from django.utils.text import gettext_lazy as _

app_name = 'kuponi'

urlpatterns = [
    path(_('dodaj/'), views.kupon_dodaj, name='dodaj'),
]
