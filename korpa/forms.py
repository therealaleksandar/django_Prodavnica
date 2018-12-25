from django import forms
from django.utils.text import gettext_lazy as _
PROIZVOD_KOLICINA_CHOICES = [(i, str(i))for i in range(1, 21)]


class KorpaDodajProizvodForma(forms.Form):
    kolicina = forms.TypedChoiceField(
        coerce=int, choices=PROIZVOD_KOLICINA_CHOICES, label=_('Kolicina'))
    azuriraj = forms.BooleanField(
        required=False, widget=forms.HiddenInput, initial=False)
