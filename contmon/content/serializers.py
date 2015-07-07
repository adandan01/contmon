from rest_framework import serializers

from .models import CreditCardOffer, CrawlUrl


class CrawlUrlSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrawlUrl
        fields = ('domain', 'path')


class CreditCardOfferSerializer(serializers.ModelSerializer):
    crawl_urls = CrawlUrlSerializer(many=True, read_only=True)
    review_states = serializers.SerializerMethodField()
    review_state_display = serializers.SerializerMethodField()

    def get_review_states(self, obj):
        return dict(CreditCardOffer.REVIEW_STATES)

    def get_review_state_display(self, obj):
        return obj.get_review_state_display()
    class Meta:
        model = CreditCardOffer
        fields = ('id', 'name', 'domain', 'image', 'review_state', 'review_state_display','review_states', 'text', 'crawl_urls')
