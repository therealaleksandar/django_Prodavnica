from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from prodavnica.models import Proizvod
from .forms import KorpaDodajProizvodForma
from .korpa import Korpa
from kuponi.forms import KuponDodajForma
from prodavnica.preporuceno import Preporucivac


@require_POST
def korpa_dodaj(request, proizvod_id):
    korpa = Korpa(request)
    proizvod = get_object_or_404(Proizvod, id=proizvod_id)
    forma = KorpaDodajProizvodForma(request.POST)
    if forma.is_valid():
        cd = forma.cleaned_data
        korpa.dodaj(proizvod=proizvod,
                    kolicina=cd['kolicina'],
                    azuriraj_kolicinu=cd['azuriraj'])
    return redirect('korpa:korpa_detaljno')


def korpa_ukloni(request, proizvod_id):
    korpa = Korpa(request)
    proizvod = get_object_or_404(Proizvod, id=proizvod_id)
    korpa.ukloni(proizvod)
    return redirect('korpa:korpa_detaljno')


def korpa_detaljno(request):
    korpa = Korpa(request)
    for predmet in korpa:
        predmet['azuriraj_kolicinu_forma'] = KorpaDodajProizvodForma(
            initial={'kolicina': predmet['kolicina'],
                     'azuriraj': True}
        )
    kupon_dodaj_forma = KuponDodajForma()
    p = Preporucivac()
    korpa_proizvodi = [predmet['proizvod'] for predmet in korpa]
    preporuceni_proizvodi = p.preporuci_proizvode_za(korpa_proizvodi)
    return render(request, 'korpa/detaljno.html', {
        'korpa': korpa,
        'kupon_dodaj_forma': kupon_dodaj_forma,
        'preporuceni_proizvodi': preporuceni_proizvodi})
