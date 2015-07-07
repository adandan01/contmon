from django.db import models
from model_utils.models import TimeStampedModel


class WebsiteScraperConfig(TimeStampedModel):

    SELECTOR_STYLE_CSS = 'css'
    SELECTOR_STYLE_XPATH = 'xpath'
    SELECTOR_STYLES = ((SELECTOR_STYLE_CSS, SELECTOR_STYLE_CSS), (SELECTOR_STYLE_XPATH, SELECTOR_STYLE_XPATH))
    domain = models.CharField(max_length=400, db_index=True)
    selector_style = models.CharField(max_length=100, blank=True, choices=SELECTOR_STYLES)
    content_selector = models.CharField(max_length=100)
    name_selector = models.CharField(max_length=100,blank=True)
    image_selector = models.CharField(max_length=100, blank=True)
    next_page_selector = models.CharField(max_length=100, blank=True)
    tabs_selector = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.domain