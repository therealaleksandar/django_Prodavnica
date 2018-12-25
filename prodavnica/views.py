from django.shortcuts import render, get_object_or_404
from korpa.forms import KorpaDodajProizvodForma
from .models import Proizvod, Kategorija
from .preporuceno import Preporucivac


def proizvodi_lista(request, kategorija_slug=None):
    kategorija = None
    kategorije = Kategorija.objects.all()
    proizvodi = Proizvod.objects.filter(dostupno=True)
    if kategorija_slug:
        jezik = request.LANGUAGE_CODE
        kategorija = get_object_or_404(Kategorija,
                                       translations__language_code=jezik,
                                       translations__slug=kategorija_slug)
        proizvodi = proizvodi.filter(kategorija=kategorija)
    return render(request,
                  'prodavnica/proizvod/lista.html', {
                      'kategorija': kategorija,
                      'kategorije': kategorije,
                      'proizvodi': proizvodi})


def proizvod_detaljno(request, id, proizvod_slug):
    jezik = request.LANGUAGE_CODE
    proizvod = get_object_or_404(Proizvod,
                                 dostupno=True,
                                 id=id,
                                 translations__language_code=jezik,
                                 translations__slug=proizvod_slug)
    korpa_proizvod_forma = KorpaDodajProizvodForma()
    p = Preporucivac()
    preporuceni_proizvodi = p.preporuci_proizvode_za([proizvod], 4)
    return render(request,
                  'prodavnica/proizvod/detaljno.html',
                  {'proizvod': proizvod,
                   'korpa_proizvod_forma': korpa_proizvod_forma,
                   'preporuceni_proizvodi': preporuceni_proizvodi})
