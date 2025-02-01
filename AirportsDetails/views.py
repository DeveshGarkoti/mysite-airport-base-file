from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Airport, Airline, Terminal, Office, Country, PlacesToVisit, Aircraft,Facility, Alias
from blog.models import Category, Post, Tag
from django.db.models import Q
from django.core.paginator import Paginator
from .utils import add_common_context  # Import the utility function
from django.http import HttpResponse
from .models import FAQ
from users.mixins import CommentContextMixin




def test(request):
    return render(request, 'AirportsDetails/test.html')


def robots_txt(request):
    content = """
    User-agent: *
    Disallow: /admin/
    Sitemap: http://airport-dot-vigilant-willow-444106-f2.uc.r.appspot.com/sitemap.xml
    """
    return HttpResponse(content, content_type="text/plain")


# Index view
class IndexView(TemplateView):
    template_name = 'AirportsDetails/index.html'
    
    # Override the context data to pass relevant models to the template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Needed for sidebar    
        context = add_common_context(context)  # Add common context

        context['countries'] = Country.objects.order_by('title')[:10]  # Show the first 5 airports
        context['places'] = PlacesToVisit.objects.filter(status='Published').order_by('-publish_date')[:10]  # Show the first 5 airports
        context['airports'] = Airport.objects.filter(status='Published').order_by('-publish_date')[:10]  # Show the first 5 airports
        context['airlines'] = Airline.objects.filter(status='Published').order_by('-publish_date')[:10]  # Show the first 5 airlines
        context['terminals'] = Terminal.objects.filter(status='Published').order_by('-publish_date')[:10]  # Show the first 5 terminals
        context['offices'] = Office.objects.filter(status='Published').order_by('-publish_date')[:10]  # Show the first 5 offices
        return context


def search(request):
    query = request.GET.get('q')
    results = []

    if query:
        # Search across all models
        airports = Airport.objects.filter(
            Q(title__icontains=query) | Q(iata_code__icontains=query) | Q(icao_code__icontains=query)
        )
        airlines = Airline.objects.filter(
            Q(title__icontains=query) | Q(iata_code__icontains=query) | Q(icao_code__icontains=query)
        )
        terminals = Terminal.objects.filter(
            Q(title__icontains=query) | Q(terminal_number__icontains=query)
        )
        offices = Office.objects.filter(
            Q(title__icontains=query) | Q(office__icontains=query)
        )
        countries = Country.objects.filter(
            Q(title__icontains=query) | Q(iso_alpha2__icontains=query)
        )
        places_to_visit = PlacesToVisit.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )
        posts = Post.objects.filter(
            Q(title__icontains=query)
        )
        faqs = FAQ.objects.filter( Q(question__icontains=query))

        # Combine all results into one list
        results = list(airports) + list(airlines) + list(terminals) + list(offices) + list(countries) + list(places_to_visit) + list(posts) + list(faqs)

    # Paginate the results
    paginator = Paginator(results, 20)  # Show 10 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {'query': query, 'page_obj': page_obj}

    # Add common context using the utility function
    context = add_common_context(context)

    # Render the search results page with the updated context
    return render(request, 'search_results.html', context)


# Airport List and Detail Views
class AirportListView(ListView):
    model = Airport
    template_name = 'AirportsDetails/airport_list.html'  # Custom template path
    context_object_name = 'airports'
    paginate_by = 20  # Optional, to paginate the list if needed

    
     # Override get_context_data to pass additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_common_context(context)  # Add common context

        return context

    
class AirportDetailView(DetailView, CommentContextMixin):
    model = Airport
    template_name = 'AirportsDetails/airport_detail.html'
    context_object_name = 'airport'

    # Override the context data to include terminals and offices related to the airport
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_common_context(context)  # Add common context

        # Pass the object_id to be used in the template
        context['object_id'] = self.object.id
        # Add comment-related context
        context.update(self.get_comment_context(self.object))

         # Filter terminals that are related to the current airline and have a status of 'Published'
        context['terminals_in_airport'] = Terminal.objects.filter(
            airport=self.object,  # Filter by related airport
            status='Published'
        ).order_by('-publish_date')[:6]

        
        context['offices_in_airport'] = Office.objects.filter(
            airport=self.object,  # Filter by related airport
            status='Published'
        ).order_by('-publish_date')[:6]

        
        context['places_to_visit_in_country'] = PlacesToVisit.objects.filter(
            country=self.object.country,  # Filter by related airport
            status='Published'
        ).order_by('-publish_date')[:6]

        context['alias_airports'] = Alias.objects.filter(
            airport=self.object,  # Filter by related airport
        )

        return context


# Airline List and Detail Views
class AirlineListView(ListView):
    model = Airline
    template_name = 'AirportsDetails/airline_list.html'
    context_object_name = 'airlines'
    paginate_by = 20  # Optional, to paginate the list if needed

    
     # Override get_context_data to pass additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_common_context(context)  # Add common context
        
        return context


class AirlineDetailView(DetailView , CommentContextMixin):
    model = Airline
    template_name = 'AirportsDetails/airline_detail.html'
    context_object_name = 'airline'

    
     # Override get_context_data to pass additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_common_context(context)  # Add common context

        # Pass the object_id to be used in the template
        context['object_id'] = self.object.id
        # Add comment-related context
        context.update(self.get_comment_context(self.object))

       # Filter terminals that are related to the current airline and have a status of 'Published'
        context['terminals_in_airline'] = Terminal.objects.filter(
            airline=self.object,  # Filter by related Airline
            status='Published'
        ).order_by('-publish_date')[:6]

        context['offices_in_airline'] = Office.objects.filter(
            airline=self.object,  # Filter by related Airline
            status='Published'
        ).order_by('-publish_date')[:6]

        context['places_to_visit_in_country'] = PlacesToVisit.objects.filter(
            country=self.object.country,  # Filter by related airport
            status='Published'
        ).order_by('-publish_date')[:6]

        context['aircrafts_airlines'] = Aircraft.objects.filter(
            airline=self.object,  # Filter by related Airline
        )


        return context


# Terminal List and Detail Views
class TerminalListView(ListView):
    model = Terminal
    template_name = 'AirportsDetails/terminal_list.html'
    context_object_name = 'terminals'
    paginate_by = 20  # Optional, to paginate the list if needed

    
    # Override get_context_data to pass additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_common_context(context)  # Add common context
        
        return context




# View to display posts filtered by category
class TerminalByAirlineView(ListView):
    model = Terminal
    template_name = 'AirportsDetails/terminal_list.html'
    context_object_name = 'terminals'
    paginate_by = 30

    def get_queryset(self):
        airline = get_object_or_404(Airline, slug=self.kwargs.get('slug'))
        return Terminal.objects.filter(airline=airline, status='Published').order_by('-publish_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['airline'] = get_object_or_404(Airline, slug=self.kwargs.get('slug'))
        
        context = add_common_context(context)  # Add common context

        return context


# View to display posts filtered by category
class TerminalByAirportView(ListView):
    model = Terminal
    template_name = 'AirportsDetails/terminal_list.html'
    context_object_name = 'terminals'
    paginate_by = 30

    def get_queryset(self):
        airport = get_object_or_404(Airport, slug=self.kwargs.get('slug'))
        return Terminal.objects.filter(airport=airport, status='Published').order_by('-publish_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['airport'] = get_object_or_404(Airport, slug=self.kwargs.get('slug'))
        
        context = add_common_context(context)  # Add common context

        return context



class TerminalDetailView(DetailView , CommentContextMixin):
    model = Terminal
    template_name = 'AirportsDetails/terminal_detail.html'
    context_object_name = 'terminal'

    
    # Override get_context_data to pass additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pass the object_id to be used in the template
        context['object_id'] = self.object.id
        # Add comment-related context
        context.update(self.get_comment_context(self.object))
        
        context = add_common_context(context)  # Add common context

        context['places_to_visit_in_country'] = PlacesToVisit.objects.filter(
            country=self.object.airport.country,  # Filter by related airport
            status='Published'
        ).order_by('-publish_date')[:6]
        

        context['terminals_in_airline'] = Terminal.objects.filter(
            airline=self.object.airline,  # Filter by related Airline
            status='Published'
        ).order_by('-publish_date')[:6]

        context['offices_in_airline'] = Office.objects.filter(
            airline=self.object.airline,  # Filter by related Airline
            status='Published'
        ).order_by('-publish_date')[:6]


         # Filter terminals that are related to the current airline and have a status of 'Published'
        context['terminals_in_airport'] = Terminal.objects.filter(
            airport=self.object.airport,  # Filter by related airport
            status='Published'
        ).order_by('-publish_date')[:6]

        
        context['offices_in_airport'] = Office.objects.filter(
            airport=self.object.airport,  # Filter by related airport
            status='Published'
        ).order_by('-publish_date')[:6]

        
        
        context['alias_airports'] = Alias.objects.filter(
            airport=self.object.airport,  # Filter by related airport
        )
        
        context['aircrafts_airlines'] = Aircraft.objects.filter(
            airline=self.object.airline,  # Filter by related Airline
        )
        

        return context


# Office List and Detail Views
class OfficeListView(ListView):
    model = Office
    template_name = 'AirportsDetails/office_list.html'
    context_object_name = 'offices'
    paginate_by = 20  # Optional, to paginate the list if needed

    
     # Override get_context_data to pass additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context = add_common_context(context)  # Add common context

        return context


# View to display posts filtered by category
class OfficeByAirlineView(ListView):
    model = Office
    template_name = 'AirportsDetails/office_list.html'
    context_object_name = 'offices'
    paginate_by = 30

    def get_queryset(self):
        airline = get_object_or_404(Airline, slug=self.kwargs.get('slug'))
        return Office.objects.filter(airline=airline, status='Published').order_by('-publish_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['airline'] = get_object_or_404(Airline, slug=self.kwargs.get('slug'))
        
        context = add_common_context(context)  # Add common context

        return context


# View to display posts filtered by category
class OfficeByAirportView(ListView):
    model = Office
    template_name = 'AirportsDetails/office_list.html'
    context_object_name = 'offices'
    paginate_by = 30

    def get_queryset(self):
        airport = get_object_or_404(Airport, slug=self.kwargs.get('slug'))
        return Office.objects.filter(airport=airport, status='Published').order_by('-publish_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['airport'] = get_object_or_404(Airport, slug=self.kwargs.get('slug'))
        
        context = add_common_context(context)  # Add common context

        return context


class OfficeDetailView(DetailView, CommentContextMixin):
    model = Office
    template_name = 'AirportsDetails/office_detail.html'
    context_object_name = 'office'

    
     # Override get_context_data to pass additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context = add_common_context(context)  # Add common context

        # Pass the object_id to be used in the template
        context['object_id'] = self.object.id
        # Add comment-related context
        context.update(self.get_comment_context(self.object))


        context['places_to_visit_in_country'] = PlacesToVisit.objects.filter(
            country=self.object.airport.country,  # Filter by related airport
            status='Published'
        ).order_by('-publish_date')[:6]
        

        context['terminals_in_airline'] = Terminal.objects.filter(
            airline=self.object.airline,  # Filter by related Airline
            status='Published'
        ).order_by('-publish_date')[:6]

        context['offices_in_airline'] = Office.objects.filter(
            airline=self.object.airline,  # Filter by related Airline
            status='Published'
        ).order_by('-publish_date')[:6]


         # Filter terminals that are related to the current airline and have a status of 'Published'
        context['terminals_in_airport'] = Terminal.objects.filter(
            airport=self.object.airport,  # Filter by related airport
            status='Published'
        ).order_by('-publish_date')[:6]

        
        context['offices_in_airport'] = Office.objects.filter(
            airport=self.object.airport,  # Filter by related airport
            status='Published'
        ).order_by('-publish_date')[:6]



        context['alias_airports'] = Alias.objects.filter(
            airport=self.object.airport,  # Filter by related airport
        )
        
        context['aircrafts_airlines'] = Aircraft.objects.filter(
            airline=self.object.airline,  # Filter by related Airline
        )
        
        return context




# List view for displaying all countries
class CountryListView(ListView):
    model = Country
    template_name = 'AirportsDetails/country_list.html'  # Specify your template name
    context_object_name = 'countries'
    paginate_by = 50  # Optional, to paginate the list if needed

    
     # Override get_context_data to pass additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = add_common_context(context)  # Add common context

        return context



# View to display posts filtered by category
class AirlineByCountryView(ListView):
    model = Airline
    template_name = 'AirportsDetails/airline_list.html'
    context_object_name = 'airlines'
    paginate_by = 20  # Optional, to paginate the list if needed
    
    def get_queryset(self):
        country = get_object_or_404(Country, slug=self.kwargs.get('slug'))
        return Airline.objects.filter(country=country, status='Published').order_by('-publish_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['country'] = get_object_or_404(Country, slug=self.kwargs.get('slug'))
        
        context = add_common_context(context)  # Add common context

        return context



# View to display posts filtered by category
class AirportByCountryView(ListView):
    model = Airport
    template_name = 'AirportsDetails/airport_list.html'
    context_object_name = 'airports'
    paginate_by = 20  # Optional, to paginate the list if needed
    
    def get_queryset(self):
        country = get_object_or_404(Country, slug=self.kwargs.get('slug'))
        return Airport.objects.filter(country=country, status='Published').order_by('-publish_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['country'] = get_object_or_404(Country, slug=self.kwargs.get('slug'))
        
        context = add_common_context(context)  # Add common context

        return context



# View to display posts filtered by category
class PlacesByCountryView(ListView):
    model = PlacesToVisit
    template_name = 'AirportsDetails/places_list.html'  # Specify your template name
    context_object_name = 'places'
    paginate_by = 10  # Optional, paginate the list

    def get_queryset(self):
        country = get_object_or_404(Country, slug=self.kwargs.get('slug'))
        return PlacesToVisit.objects.filter(country=country, status='Published').order_by('-publish_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['country'] = get_object_or_404(Country, slug=self.kwargs.get('slug'))
        
        context = add_common_context(context)  # Add common context

        return context



# Detail view for displaying a specific country's details
class CountryDetailView(DetailView, CommentContextMixin):
    model = Country
    template_name = 'AirportsDetails/country_detail.html'  # Specify your template name
    context_object_name = 'country'

    def get_object(self):
        # Fetch the country by its slug
        return get_object_or_404(Country, slug=self.kwargs.get('slug'))
    
    
     # Override get_context_data to pass additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context = add_common_context(context)  # Add common context
        
        # Pass the object_id to be used in the template
        context['object_id'] = self.object.id
        # Add comment-related context

        context.update(self.get_comment_context(self.object))

        context['airlines_in_country'] = Airline.objects.filter(
            country=self.object,  # Filter by related Airline
            status='Published'
        ).order_by('-publish_date')[:6]

        
        context['airports_in_country'] = Airport.objects.filter(
            country=self.object,  # Filter by related Airline
            status='Published'
        ).order_by('-publish_date')[:6]

        context['places_to_visit_in_country'] = PlacesToVisit.objects.filter(
            country=self.object,  # Filter by related Airline
            status='Published'
        ).order_by('-publish_date')[:6]



        return context

    

# List view for displaying all places to visit
class PlacesToVisitListView(ListView):
    model = PlacesToVisit
    template_name = 'AirportsDetails/places_list.html'  # Specify your template name
    context_object_name = 'places'
    paginate_by = 10  # Optional, paginate the list

    
     # Override get_context_data to pass additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_common_context(context)  # Add common context
        

        return context


# Detail view for displaying a specific place based on slug
class PlacesToVisitDetailView(DetailView, CommentContextMixin):
    model = PlacesToVisit
    template_name = 'AirportsDetails/places_detail.html'  # Specify your template name
    context_object_name = 'place'


    def get_object(self):
        # Fetch the place by its slug
        return get_object_or_404(PlacesToVisit, slug=self.kwargs.get('slug'))
    
    
     # Override get_context_data to pass additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context = add_common_context(context)  # Add common context
        # Pass the object_id to be used in the template
        context['object_id'] = self.object.id
        # Add comment-related context
        context.update(self.get_comment_context(self.object))

        return context



class FAQListView(ListView):
    model = FAQ
    template_name = 'faq/faq_list.html'
    context_object_name = 'faqs'
    queryset = FAQ.objects.all()  # Adjust if you have a status field
    paginate_by = 30 

    
     # Override get_context_data to pass additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_common_context(context)  # Add common context
        
        return context




class FAQDetailView(CommentContextMixin, DetailView):
    model = FAQ
    template_name = 'faq/faq_detail.html'
    context_object_name = 'faq'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = add_common_context(context)  # Add common context

        # Pass the object_id to be used in the template
        context['object_id'] = self.object.id
        # Add comment-related context
        context.update(self.get_comment_context(self.object))
        return context