from haystack import indexes
from .models import CrawledPage, CreditCardOffer


class CreditCardOfferIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    domain = indexes.CharField(model_attr='domain')

    def get_model(self):
        return CreditCardOffer

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class CrawledPageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return CrawledPage

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()
