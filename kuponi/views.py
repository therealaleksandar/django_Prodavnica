from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Kupon
from .forms import KuponDodajForma


@require_POST
def kupon_dodaj(request):
    forma = KuponDodajForma(request.POST)
    if forma.is_valid():
        kod = forma.cleaned_data['kod']
        try:
            kupon = Kupon.objects.get(kod__iexact=kod,
                                      vazi_od__lte=timezone.now(),
                                      vazi_do__gte=timezone.now(),
                                      aktivno=True)
            request.session['kupon_id'] = kupon.id
        except Kupon.DoesNotExist:
            request.session['kupon_id'] = None
    return redirect('korpa:korpa_detaljno')
