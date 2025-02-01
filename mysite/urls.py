"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap
from .sitemaps import PostSitemap, AirlineSitemap,AirportSitemap,TerminalSitemap,OfficeSitemap, PlacesToVisitSitemap, CountrySitemap, StaticViewSitemap, AirlinesTerminalSitemap, AirlinesOfficeSitemap, AirportsOfficeSitemap, AirportsTerminalSitemap, FAQSitemap


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blogs/', include('blog.urls')),
    path('', include('AirportsDetails.urls') ),
    path('users/', include('users.urls')),
]

# Serve media files during development

urlpatterns += [
    # Other paths
    path('ckeditor/', include('django_ckeditor_5.urls')),  # For CKEditor 5 file uploads
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Sitemaps

sitemaps_index = {
    'static': StaticViewSitemap,
}

sitemaps_posts = {
    'posts': PostSitemap,
}

sitemaps_airlines = {
    'airlines': AirlineSitemap,
}

sitemaps_airlines_terminals = {
    'airlines': AirlinesTerminalSitemap,
}

sitemaps_airlines_offices = {
    'airlines': AirlinesOfficeSitemap,
}


sitemaps_airports_terminals = {
    'airports': AirportsTerminalSitemap,
}

sitemaps_airports_offices = {
    'airports': AirportsOfficeSitemap,
}


sitemaps_airports = {
    'airports': AirportSitemap,
}

sitemaps_terminals = {
    'terminals': TerminalSitemap,
}



sitemaps_offices = {
    'offices': OfficeSitemap,
}

sitemaps_places = {
    'places': PlacesToVisitSitemap,
}

sitemaps_countries = {
    'countries': CountrySitemap,
}

sitemaps_faqs = {
    'faqs': FAQSitemap,
}

urlpatterns += [
    # Other URL patterns...
    path('sitemap-posts.xml', sitemap, {'sitemaps': sitemaps_posts}, name='sitemap-posts'),
    path('sitemap-airlines.xml', sitemap, {'sitemaps': sitemaps_airlines}, name='sitemap-airlines'),
    path('sitemap-airlines-terminals.xml', sitemap, {'sitemaps': sitemaps_airlines_terminals}, name='sitemap-airlines-terminals'),
    path('sitemap-airlines-offices.xml', sitemap, {'sitemaps': sitemaps_airlines_offices}, name='sitemap-airlines-offices'),
    path('sitemap-airports-terminals.xml', sitemap, {'sitemaps': sitemaps_airports_terminals}, name='sitemap-airports-terminals'),
    path('sitemap-airports-offices.xml', sitemap, {'sitemaps': sitemaps_airports_offices}, name='sitemap-airports-offices'),
    path('sitemap-airports.xml', sitemap, {'sitemaps': sitemaps_airports}, name='sitemap-airports'),
    path('sitemaps-terminals.xml', sitemap, {'sitemaps': sitemaps_terminals}, name='sitemaps-terminals'),
    path('sitemap-offices.xml', sitemap, {'sitemaps': sitemaps_offices}, name='sitemap-offices'),
    path('sitemap-places.xml', sitemap, {'sitemaps': sitemaps_places}, name='sitemap-places'),
    path('sitemap-countries.xml', sitemap, {'sitemaps': sitemaps_countries}, name='sitemap-countries'),
    path('sitemap-faqs.xml', sitemap, {'sitemaps': sitemaps_faqs}, name='sitemap-faqs'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps_index}, name='sitemap'),
]