from django import forms
from django.utils.text import gettext_lazy as _


class KuponDodajForma(forms.Form):
    kod = forms.CharField(label=_('Kupon'))
