from django.contrib import admin
from .models import CrawlUrl, CrawledPage, CreditCardOffer
from reversion_compare.admin import CompareVersionAdmin

@admin.register(CrawlUrl, CrawledPage)
class CrawlContentAdmin(CompareVersionAdmin):
    pass

@admin.register(CreditCardOffer)
class CreditCardOfferADmin(CompareVersionAdmin):
    readonly_fields = ('extracted_fields',)
    list_display = ('domain',)
    list_filter = ('domain',)