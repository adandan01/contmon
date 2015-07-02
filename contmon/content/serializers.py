from rest_framework import serializers

from .models import CreditCardOffer, CrawlUrl


class CrawlUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlUrl
        fields = ('domain', 'path')


class CreditCardOfferSerializer(serializers.ModelSerializer):
    crawl_urls = CrawlUrlSerializer(many=True, read_only=True)

    class Meta:
        model = CreditCardOffer
        fields = ('id', 'name', 'domain', 'image', 'text', 'crawl_urls')
