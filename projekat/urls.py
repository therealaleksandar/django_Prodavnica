"""projekat URL confuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.utils.text import gettext_lazy as _

urlpatterns = i18n_patterns(
    path(_('admin/'), admin.site.urls),
    path(_('korpa/'), include('korpa.urls', namespace='korpa')),
    path(_('narudzbina/'), include('narudzbina.urls', namespace='narudzbina')),
    path(_('placanje/'), include('placanje.urls', namespace='placanje')),
    path(_('kuponi/'), include('kuponi.urls', namespace='kuponi')),
    path('rosetta/', include('rosetta.urls')),
    path('', include('prodavnica.urls', namespace='prodavnica')),
)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
