from django.urls import path
from . import views
from django.utils.text import gettext_lazy as _

app_name = 'placanje'

urlpatterns = [
    path(_('proces/'), views.placanje_proces, name='proces'),
    path(_('gotovo/'), views.placanje_gotovo, name='gotovo'),
    path(_('otkazano/'), views.placanje_otkazano, name='otkazano'),
]
