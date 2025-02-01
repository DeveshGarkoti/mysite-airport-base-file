from django.urls import path
from . import views


urlpatterns = [
    # Index view URL
    path('', views.IndexView.as_view(), name='index'),
    path('', views.IndexView.as_view(), name='home'),
    
    path('test',views.test, name='test'),
    path('robots.txt', views.robots_txt, name='robots_txt'),

    # Search functionality
    path('search/', views.search, name='search'),
    
    # Airport URLs
    path('airports/', views.AirportListView.as_view(), name='airport_list'),
    path('airports/<slug:slug>/', views.AirportDetailView.as_view(), name='airport_detail'),

    # Airline URLs
    path('airlines/', views.AirlineListView.as_view(), name='airline_list'),
    path('airlines/<slug:slug>/', views.AirlineDetailView.as_view(), name='airline_detail'),

    # Terminal URLs
    path('terminals/', views.TerminalListView.as_view(), name='terminal_list'),

    path('terminals/<slug:slug>/', views.TerminalDetailView.as_view(), name='terminal_detail'),
    
    # URL for filtering Terminals by Airlines
    path('terminals/airlines/<slug:slug>/', views.TerminalByAirlineView.as_view(), name='terminals_by_airline_list'),

    # URL for filtering Terminals by Airport
    path('terminals/airports/<slug:slug>/', views.TerminalByAirportView.as_view(), name='terminals_by_airport_list'),


    # Office URLs
    path('offices/', views.OfficeListView.as_view(), name='office_list'),

    path('offices/<slug:slug>/', views.OfficeDetailView.as_view(), name='office_detail'),


    # URL for filtering offices by Airlines
    path('offices/airlines/<slug:slug>/', views.OfficeByAirlineView.as_view(), name='offices_by_airline_list'),

    # URL for filtering offices by Airport
    path('offices/airports/<slug:slug>/', views.OfficeByAirportView.as_view(), name='offices_by_airport_list'),

    # URL for country list
    path('countries/', views.CountryListView.as_view(), name='country_list'),
    
    # URL for country detail (slug-based)
    path('countries/<slug:slug>/', views.CountryDetailView.as_view(), name='country_detail'),

    path('countries/airlines/<slug:slug>/', views.AirlineByCountryView.as_view(), name='airlines_by_country_list'),

    path('countries/airport/<slug:slug>/', views.AirportByCountryView.as_view(), name='airport_by_country_list'),

    path('countries/places-to-visit/<slug:slug>/', views.PlacesByCountryView.as_view(), name='places_to_visit_by_country_list'),

    # URL for places to visit list
    path('places-to-visit/', views.PlacesToVisitListView.as_view(), name='places_list'),
    
    # URL for place details (slug-based)
    path('places-to-visit/<slug:slug>/', views.PlacesToVisitDetailView.as_view(), name='place_detail'),

    path('faqs/', views.FAQListView.as_view(), name='faq_list'),
    path('faqs/<slug:slug>/', views.FAQDetailView.as_view(), name='faq_detail'),

]
