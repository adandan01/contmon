from django.contrib import admin
from reversion_compare.admin import CompareVersionAdmin
from .models import WebsiteScraperConfig

@admin.register(WebsiteScraperConfig)
class ScraperConfigAdmin(CompareVersionAdmin):
    pass