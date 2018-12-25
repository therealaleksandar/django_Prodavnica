from django import forms
from .models import Narudzbina


class NarudzbinaForma(forms.ModelForm):
    class Meta:
        model = Narudzbina
        fields = ['ime', 'prezime', 'email',
                  'adresa', 'mesto', 'postanski_broj']
