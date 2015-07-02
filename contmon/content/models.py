from django.db import models

# Create your models here.

# class ContMonWebsite(models.Model):
#     pass

class CrawlUrl(models.Model):
    url = models.CharField(max_length=500, db_index=True)
    domain = models.CharField(max_length=400, db_index=True)
    path = models.CharField(max_length=400)
    crawled_on = models.DateField(blank=True, null=True)

class CrawledPage(models.Model):
    crawl_url = models.ForeignKey(CrawlUrl)
    page_number = models.IntegerField()
    image = models.ImageField(upload_to='crawled_page')
    text = models.TextField(blank=True)
    content_hash = models.CharField(max_length=500, db_index=True)


class AbstractExtractedContent(models.Model):
    crawl_urls = models.ManyToManyField(CrawlUrl)
    domain = models.CharField(max_length=400, db_index=True, default='')
    image = models.ImageField(upload_to='extracted_content')
    location_x = models.FloatField()
    location_y = models.FloatField()
    size_width = models.FloatField()
    size_height = models.FloatField()
    content_hash = models.CharField(max_length=500, db_index=True)
    text = models.TextField(blank=True)
    #TODO should reference the extractor
    class Meta:
        abstract = True
        unique_together = ("domain", "content_hash")



class CreditCardOffer(AbstractExtractedContent):
    @property
    def name(self):
        return self.text.split('\n')[0]


# class ComplianceViolation(models.Model):
#     pass
#
# class Extractor(models.Model):
#     pass



