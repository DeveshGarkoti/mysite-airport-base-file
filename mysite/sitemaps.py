from django.contrib.sitemaps import Sitemap
from blog.models import Post, Category, Tag  # Import your model
from AirportsDetails.models import Airline, Airport, Terminal, Office, Country, PlacesToVisit, FAQ
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.9

    # This method returns a list of names of the static views you want to include
    def items(self):
        return ['index','robots_txt','airport_list', 'airline_list','terminal_list','office_list' ,'country_list', 'places_list','sitemap-posts','sitemap-airlines','sitemap-airports', 'sitemaps-terminals', 'sitemap-offices','sitemap-places','sitemap-countries','sitemap-airlines-terminals', 'sitemap-airlines-offices','sitemap-airports-terminals', 'sitemap-airports-offices','sitemap-faqs']

    # This method converts each static view into a full URL using Django's `reverse`
    def location(self, item):
        return reverse(item)



class FAQSitemap(Sitemap):
    changefreq = "weekly"  # Frequency of expected updates
    priority = 0.8  # Priority level for search engines (0.0 to 1.0)

    def items(self):
        return FAQ.objects.all()  # Adjust if there's a status field

    def location(self, obj):
        return obj.get_absolute_url()



class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.update_date
    

    def location(self, obj):
        return f'/blog/post/{obj.slug}/'


class AirportSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Airport.objects.filter(status='Published')

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return f'/airports/{obj.slug}/'
    



class AirlineSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Airline.objects.filter(status='Published')

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return f'/airlines/{obj.slug}/'  # The URL for each airline



class TerminalSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Terminal.objects.filter(status='Published')

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return f'/terminals/{obj.slug}/'
    

class AirlinesTerminalSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Airline.objects.filter(status='Published')

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return f'/terminals/airlines/{obj.slug}/'
    


class AirlinesOfficeSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Airline.objects.filter(status='Published')

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return f'/offices/airlines/{obj.slug}/'
    


class AirportsTerminalSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Airport.objects.filter(status='Published')

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return f'/terminals/airports/{obj.slug}/'
    


class AirportsOfficeSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Airport.objects.filter(status='Published')

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return f'/offices/airports/{obj.slug}/'
   

class OfficeSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Office.objects.filter(status='Published')

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return f'/offices/{obj.slug}/'
    


class PlacesToVisitSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return PlacesToVisit.objects.filter(status='Published')

    def lastmod(self, obj):
        return obj.update_date

    def location(self, obj):
        return f'/places-to-visit/{obj.slug}/'
    


class CountrySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Country.objects.all()

    def location(self, obj):
        return f'/countries/{obj.slug}/'
    
