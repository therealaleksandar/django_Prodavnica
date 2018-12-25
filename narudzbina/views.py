from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import NarudzbinaPredmet, Narudzbina
from .forms import NarudzbinaForma
from korpa.korpa import Korpa
from .tasks import narudzbina_kreirana


def narudzbina_dodaj(request):
    korpa = Korpa(request)
    if request.method == 'POST':
        forma = NarudzbinaForma(request.POST)
        if forma.is_valid():
            narudzbina = forma.save(commit=False)
            if korpa.kupon:
                narudzbina.kupon=korpa.kupon
                narudzbina.popust = korpa.kupon.popust
            narudzbina.save()
            for predmet in korpa:
                NarudzbinaPredmet.objects.create(narudzbina=narudzbina,
                                                 proizvod=predmet['proizvod'],
                                                 kolicina=predmet['kolicina'],
                                                 cena=predmet['cena'])
            korpa.ocisti()
            narudzbina_kreirana.delay(narudzbina.id)
            request.session['narudzbina_id'] = narudzbina.id
            return redirect(reverse('placanje:proces'))
    else:
        forma = NarudzbinaForma()
    return render(request, 'narudzbina/kreiraj.html', {'forma': forma})


@staff_member_required
def admin_narudzbina_detaljno(request, narudzbina_id):
    narudzbina = get_object_or_404(Narudzbina, id=narudzbina_id)
    return render(request, 'admin/narudzbina/detaljno.html', {'narudzbina': narudzbina})


@staff_member_required
def admin_narudzbina_pdf(request, narudzbina_id):
    narudzbina = get_object_or_404(Narudzbina, id=narudzbina_id)
    html = render_to_string('narudzbina/pdf.html', {'narudzbina': narudzbina})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="narudzbina_{}.pdf"'.format(narudzbina.id)
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[
        weasyprint.CSS(settings.STATIC_ROOT+'pdf.css')
    ])
    return response
