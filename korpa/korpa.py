from decimal import Decimal
from django.conf import settings
from prodavnica.models import Proizvod
from kuponi.models import Kupon


class Korpa(object):
    def __init__(self, request):
        """ Inicijalizuje korpu. """
        self.session = request.session
        korpa = self.session.get(settings.KORPA_SESSION_ID)
        if not korpa:
            # Sacuvaj praznu korpu u session
            korpa = self.session[settings.KORPA_SESSION_ID] = {}
        self.korpa = korpa
        self.kupon_id = self.session.get('kupon_id')

    @property
    def kupon(self):
        if self.kupon_id:
            return Kupon.objects.get(id=self.kupon_id)
        return None

    def dobij_popust(self):
        if self.kupon:
            return self.dobij_punu_cenu()*(self.kupon.popust/Decimal('100'))
        return Decimal('0')

    def dobij_punu_cenu_posle_popusta(self):
        return self.dobij_punu_cenu()-self.dobij_popust()

    def dodaj(self, proizvod, kolicina=1, azuriraj_kolicinu=False):
        """ Dodaj proizvod u korpu ili azuriraj kolicinu """
        proizvod_id = str(proizvod.id)
        if proizvod_id not in self.korpa:
            self.korpa[proizvod_id] = {
                'kolicina': 0, 'cena': str(proizvod.cena)}
        if azuriraj_kolicinu:
            self.korpa[proizvod_id]['kolicina'] = kolicina
        else:
            self.korpa[proizvod_id]['kolicina'] += kolicina
        self.sacuvaj()

    def sacuvaj(self):
        # ovo kaze djangu da je sesija promenjena i da treba da se sacuva
        self.session.modified = True

    def ukloni(self, proizvod):
        """ Ukloni proizvod iz korpe. """
        proizvod_id = str(proizvod.id)
        if proizvod_id in self.korpa:
            del self.korpa[proizvod_id]
            self.sacuvaj()

    def __iter__(self):
        """ Prolazi kroz proizvode u korpi i vadi ih iz baze """
        proizvodi_ids = self.korpa.keys()
        # dobij proizvode i dodaj ih u korpu
        proizvodi = Proizvod.objects.filter(id__in=proizvodi_ids)
        korpa = self.korpa.copy()
        for proizvod in proizvodi:
            korpa[str(proizvod.id)]['proizvod'] = proizvod

        for predmet in korpa.values():
            predmet['cena'] = Decimal(predmet['cena'])
            predmet['puna_cena'] = predmet['cena']*predmet['kolicina']
            yield predmet

    def __len__(self):
        """ Izbroj sve predmete u korpi. """
        return sum(predmet['kolicina'] for predmet in self.korpa.values())

    def dobij_punu_cenu(self):
        return sum(
            Decimal(predmet['cena']) * predmet['kolicina'] for predmet in
            self.korpa.values())

    def ocisti(self):
        # ocisti korpu
        del self.session[settings.KORPA_SESSION_ID]
        self.sacuvaj()
