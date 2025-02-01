from django.contrib import admin
from .models import Airport, Airline, Terminal, Office
from django.contrib import admin
from .models import Facility, Alias, PlacesToVisit, FAQ, Aircraft, Country, Service


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('title',)  # Adjust according to your Country model fields
    search_fields = ('title',)  # Enable search on the country title

    prepopulated_fields = {'slug': ('title',)} # 

    filter_horizontal = ('faqs','places_to_visit')  # Allow Many-to-Many FAQ selection in a user-friendly manner


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)



@admin.register(Service)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)



class AliasInline(admin.TabularInline):
    model = Alias
    extra = 1


# Aircraft Inline
class AircraftInline(admin.TabularInline):
    model = Aircraft
    extra = 1  # Number of blank forms to display for adding new aircraft



class FAQInline(admin.TabularInline):  # Or use admin.StackedInline for a different layout
    model = FAQ
    extra = 1  # Number of empty FAQ forms to show by default


@admin.register(FAQ)    
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'meta_title', 'slug', 'preview_answer')
    search_fields = ('question', 'answer', 'meta_title', 'meta_description')
    prepopulated_fields = {"slug": ("question",)}
    list_filter = ('meta_title',)
    
    def preview_answer(self, obj):
        return obj.answer[:50] + '...' if len(obj.answer) > 50 else obj.answer
    preview_answer.short_description = 'Answer Preview'



@admin.register(PlacesToVisit)
class PlacesToVisitAdmin(admin.ModelAdmin):
    list_display = ('title', 'country', 'status', 'publish_date', 'update_date')  # Fields to display in the admin list
    list_filter = ('status', 'country')  # Filters by status and country
    search_fields = ('title', 'meta_title', 'content')  # Searchable fields
    prepopulated_fields = {'slug': ('meta_title',)}  # Auto-fill slug based on title
    filter_horizontal = ('faqs',)  # Allow Many-to-Many FAQ selection in a user-friendly manner
    autocomplete_fields = ('country',) # for Foriegn key filter

    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'meta_title', 'slug', 'meta_keywords', 'meta_description', 'content', 'country', 'faqs','embed_code','embed_map' )
        }),
        ('Photo Information', {
            'fields': ('photo', 'photo_alt')
        }),
        ('Status and Dates', {
            'fields': ('status', 'publish_date')
        }),
    )


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('title', 'iata_code', 'icao_code', 'operational', 'status')
    list_filter = ('operational', 'airport_type', 'status')
    search_fields = ('title', 'iata_code')  # Add search capability, including country name
    prepopulated_fields = {'slug': ('meta_title',)} # 
    filter_horizontal = ('facilities_available','faqs')  # Optional: shows a horizontal filter widget for M2M fields
    inlines = [ AliasInline]  # Adding FAQ Inline to Airport
    autocomplete_fields = ('country',) # for Foriegn key filter

    # Customizing the fieldsets to group related fields
    fieldsets = (
        (None, {
            'fields': ('title', 'meta_title', 'slug', 'meta_keywords', 'meta_description')
        }),
        ('Airport Details', {
            'fields': ('iata_code', 'icao_code', 'airport_type', 'operational', 'airport_size', 'area_served', 'content','facilities_available','faqs', 'embed_code','embed_map'),
        }),
        ('Google Map Section', {
            'fields': ('location', 'website', 'contact_info', 'maps_link', 'country'),
        }),
        ('Social Media Links Section', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url'),
        }),
        ('Photo Section', {
            'fields': ('photo', 'photo_alt'),
        }),
        ('Status and Layout', {
            'fields': ('status', 'publish_date', 'layout'),
        }),
    )
    


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('title', 'iata_code', 'icao_code', 'operational', 'status')
    list_filter = ('operational', 'status')
    search_fields = ('title', 'iata_code', 'icao_code', 'meta_title', 'meta_keywords')
    prepopulated_fields = {'slug': ('meta_title',)}
    inlines = [ AircraftInline]  # Adding FAQ Inline to Airport
    filter_horizontal = ('faqs','services_available')
    autocomplete_fields = ('country',) # for Foriegn key filter

    
    fieldsets = (
        (None, {
            'fields': ('title', 'meta_title', 'slug', 'meta_keywords', 'meta_description')
        }),
        ('Airlines Details', {
            'fields': ('iata_code', 'icao_code', 'headquarters', 'operational', 'area_served','content','faqs', 'embed_code','services_available'),
        }),
        ('Google Map Section', {
            'fields': ('location', 'website', 'contact_info', 'map_link', 'country'),
        }),
        ('Social Media Links Section', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url'),
        }),
        ('Photo Section', {
            'fields': ('photo', 'photo_alt'),
        }),
        ('Status and Layout', {
            'fields': ('status',  'publish_date', 'layout'),
        }),
    )

# # Register the Airport model with the customized admin class


@admin.register(Terminal)
class TerminalAdmin(admin.ModelAdmin):
    list_display = ('title', 'terminal_number', 'airport', 'airline', 'status')
    list_filter = ('status', 'airport', 'airline')
    search_fields = ('title', 'meta_title', 'meta_keywords')
    prepopulated_fields = {'slug': ('meta_title',)}
    filter_horizontal = ('faqs',)
    search_fields = ('title', 'airport__title', 'airline__title', 'meta_title', 'meta_keywords', 'meta_description')  # Searchable fields including airport and airline titles
    autocomplete_fields = ('airport','airline') # for Foriegn key filter
    

    fieldsets = (
        (None, {
            'fields': ('title', 'terminal_number','meta_title',  'slug', 'meta_keywords', 'meta_description')
        }),
        ('Content Section', {
            'fields': ('airport', 'airline','content','faqs','embed_code' ),
        }),
        ('Photo Section', {
            'fields': ('photo', 'photo_alt'),
        }),
        ('Status and Layout', {
            'fields': ('status', 'publish_date', 'layout'),
        }),
    )


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('title', 'office', 'airport', 'airline', 'status')
    list_filter = ('status', 'airport', 'airline')
    search_fields = ('title', 'meta_title', 'meta_keywords', 'airport__title', 'airline__title')
    prepopulated_fields = {'slug': ('meta_title',)}
    filter_horizontal = ('faqs',)
    autocomplete_fields = ('airport','airline') # for Foriegn key filter


    fieldsets = (
        (None, {
            'fields': ('title', 'office','meta_title', 'slug',  'meta_keywords', 'meta_description')
        }),
        ('Content Section', {
            'fields': ('airport', 'airline','content','faqs','embed_code'),
        }),
        ('Photo Section', {
            'fields': ('photo', 'photo_alt'),
        }),
        ('Necessary Section', {
            'fields': ('status', 'publish_date', 'layout'),
        }),
    )
