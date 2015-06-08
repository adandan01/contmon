from django.contrib import admin
from .models import CrawlUrl, CrawledPage, CreditCardOffer


@admin.register(CrawlUrl, CrawledPage, CreditCardOffer)
class CrawlContentAdmin(admin.ModelAdmin):
    pass