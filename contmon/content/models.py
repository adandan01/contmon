from django.db import models

# Create your models here.

# class ContMonWebsite(models.Model):
#     pass
from jsonfield import JSONField
from model_utils.models import TimeStampedModel
import reversion


class CrawlUrl(TimeStampedModel):
    url = models.CharField(max_length=500, db_index=True)
    domain = models.CharField(max_length=400, db_index=True)
    path = models.CharField(max_length=400)

    def __unicode__(self):
        return self.url

class CrawledPage(TimeStampedModel):
    crawl_url = models.ForeignKey(CrawlUrl)
    page_number = models.IntegerField()
    image = models.ImageField(upload_to='crawled_page')
    text = models.TextField(blank=True)
    content_hash = models.CharField(max_length=500, db_index=True)

    def __unicode__(self):
        return "crawled page: %s page number:" % (self.crawl_url, self.page_number)


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
    REVIEW_STATES_DICT = dict(REVIEW_STATES)
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

    @property
    def review_state_change_history(self):
        available_versions = list(reversion.get_for_object(self)[:20])
        history_log = []
        for i, version in enumerate(available_versions):
            if i < (len(available_versions)-1) :
                old_version = available_versions[i+1]
                new_version = available_versions[i]
                field_name = 'review_state'
                old_text = old_version.field_dict.get(field_name, "")
                new_text = new_version.field_dict.get(field_name, "")
                message = "<del><span class='bg-warning'>%s</span></del>  <ins><span class='bg-info'>%s</span></ins>" % (self.REVIEW_STATES_DICT[old_text], self.REVIEW_STATES_DICT[new_text])
                history_log.append({'user':version.revision.user.username if version.revision.user else '','date': version.revision.date_created.strftime('%B %d., %Y, %I:%M%p:%S'), 'patch_html':message })

        return history_log


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



