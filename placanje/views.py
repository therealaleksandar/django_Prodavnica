import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import weasyprint
from io import BytesIO
from narudzbina.models import Narudzbina


def placanje_proces(request):
    narudzbina_id = request.session.get('narudzbina_id')
    narudzbina = get_object_or_404(Narudzbina, id=narudzbina_id)

    if request.method == 'POST':
        nonce = request.POST.get('payment_method_nonce', None)
        rezultat = braintree.Transaction.sale({
            'amount': '{:.2f}'.format(narudzbina.dobij_punu_cenu_posle_popusta()),
            'payment_method_nonce': nonce,
            'options': {
                'submit_for_settlement': True
            }
        })
        if rezultat.is_success:
            narudzbina.placeno = True
            narudzbina.braintree_id = rezultat.transaction.id
            narudzbina.save()
            # kreiranje mejla sa predracunom
            subjekat = 'Prodavnica - Predracun br.{}'.format(narudzbina.id)
            poruka = 'Prikacen Vam je predracun za vasu kupovinu'
            email = EmailMessage(
                subjekat, poruka, 'admin@prodanvica.com', [narudzbina.email])
            # generisi PDF
            html = render_to_string('narudzbina/pdf.html', {'narudzbina': narudzbina})
            out = BytesIO()
            stylesheets = [weasyprint.CSS(settings.STATIC_ROOT+'pdf.css')]
            weasyprint.HTML(string=html).write_pdf(out, stylesheets)
            email.attach('narudzbina_{}.pdf'.format(narudzbina.id),
                         out.getvalue(), 'application/pdf')
            email.send()
            return redirect('placanje:gotovo')
        else:
            return redirect('placanje:otkazano')
    else:
        klijent_token = braintree.ClientToken.generate()
        return render(request, 'placanje/proces.html', {'narudzbina': narudzbina,
                                                        'klijent_token': klijent_token})


def placanje_gotovo(request):
    return render(request, 'placanje/gotovo.html')


def placanje_otkazano(request):
    return render(request, 'placanje/otkazano.html')
