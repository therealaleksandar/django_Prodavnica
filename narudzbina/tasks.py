from celery import task
from django.core.mail import send_mail
from .models import Narudzbina


@task
def narudzbina_kreirana(narudzbina_id):
    """ Zadatak da se posalje mejl kada je narudzbina uspesno kreirana """
    narudzbina = Narudzbina.objects.get(id=narudzbina_id)
    subjekat = 'Narudzbina br. {}'.format(narudzbina.id)
    poruka = 'Postovani {},\n\nuspesno ste narucili robu.\
    Vas broj narudzbine je {}.\n\nVasa Prodavnica.'.format(narudzbina.ime,
                                                           narudzbina.id)
    mejl_poslat = send_mail(
        subjekat, poruka, 'admin@prodavnica.com', [narudzbina.email])
    return mejl_poslat
