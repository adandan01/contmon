from django.db import models

# Create your models here.

# class ContMonWebsite(models.Model):
#     pass
from jsonfield import JSONField
from model_utils.models import TimeStampedModel


class CrawlUrl(TimeStampedModel):
    url = models.CharField(max_length=500, db_index=True)
    domain = models.CharField(max_length=400, db_index=True)
    path = models.CharField(max_length=400)

class CrawledPage(TimeStampedModel):
    crawl_url = models.ForeignKey(CrawlUrl)
    page_number = models.IntegerField()
    image = models.ImageField(upload_to='crawled_page')
    text = models.TextField(blank=True)
    content_hash = models.CharField(max_length=500, db_index=True)


class AbstractExtractedContent(TimeStampedModel):
    REVIEW_STATES_NEVER_REVIEWED = 0
    REVIEW_STATES_COMPLIANT = 1
    REVIEW_STATES_NOT_COMPLIANT = 2
    REVIEW_STATES_IRRELEVANT = 3
    REVIEW_STATES_NEVER_REVIEWED_LABEL = 'Never Reviewed'
    REVIEW_STATES_COMPLIANT_LABEL = 'Compliant'
    REVIEW_STATES_NOT_COMPLIANT_LABEL = 'Not Compliant'
    REVIEW_STATES_IRRELEVANT_LABEL = 'Irrelevant: Ignore'

    REVIEW_STATES = (
        (REVIEW_STATES_NEVER_REVIEWED, REVIEW_STATES_NEVER_REVIEWED_LABEL),
        (REVIEW_STATES_COMPLIANT, REVIEW_STATES_COMPLIANT_LABEL),
        (REVIEW_STATES_NOT_COMPLIANT, REVIEW_STATES_NOT_COMPLIANT_LABEL),
        (REVIEW_STATES_IRRELEVANT, REVIEW_STATES_IRRELEVANT_LABEL),
    )
    crawl_urls = models.ManyToManyField(CrawlUrl)
    domain = models.CharField(max_length=400, db_index=True, default='')
    image = models.ImageField(upload_to='extracted_content')
    html = models.FileField(upload_to='html')
    extracted_fields = JSONField()
    location_x = models.FloatField()
    location_y = models.FloatField()
    size_width = models.FloatField()
    size_height = models.FloatField()
    content_hash = models.CharField(max_length=500, db_index=True)
    text = models.TextField(blank=True)
    review_state = models.SmallIntegerField(choices=REVIEW_STATES, db_index=True, default=REVIEW_STATES_NEVER_REVIEWED)

    #TODO should reference the extractor
    class Meta:
        abstract = True
        unique_together = ("domain", "content_hash")



class CreditCardOffer(AbstractExtractedContent):
    @property
    def name(self):
        return self.extracted_fields.get('name', '')


# class ComplianceViolation(models.Model):
#     pass
#
# class Extractor(models.Model):
#     pass



