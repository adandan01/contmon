from django.contrib import admin
from .models import CrawlUrl, CrawledPage, CreditCardOffer
from reversion_compare.admin import CompareVersionAdmin

@admin.register(CrawlUrl)
class CrawlUrlAdmin(CompareVersionAdmin):
    list_display = ('url', 'domain',)
    list_filter = ('domain',)

@admin.register(CrawledPage)
class CrawledPageAdmin(CompareVersionAdmin):
    pass

@admin.register(CreditCardOffer)
class CreditCardOfferADmin(CompareVersionAdmin):
    readonly_fields = ('extracted_fields',)
    list_display = ('domain','name', 'created')
    list_filter = ('domain',)