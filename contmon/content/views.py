# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.db.models import Count
from django.views.generic import DetailView, ListView
from braces.views import LoginRequiredMixin
from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_extensions.cache.mixins import ListCacheResponseMixin

from .serializers import CreditCardOfferDetailSerializer, CreditCardOfferListSerializer
from .models import CrawledPage, CreditCardOffer


class CrawledPageDetailView(LoginRequiredMixin, DetailView):
    model = CrawledPage
    # These next two lines tell the view to index lookups by username
    slug_field = "id"
    slug_url_kwarg = "id"


class CrawledPageListView(LoginRequiredMixin, ListView):
    model = CrawledPage
    # These next two lines tell the view to index lookups by username
    slug_field = "id"
    slug_url_kwarg = "id"


class CreditCardOfferDetailView(LoginRequiredMixin, DetailView):
    model = CreditCardOffer
    # These next two lines tell the view to index lookups by username
    slug_field = "id"
    slug_url_kwarg = "id"


class CreditCardOfferListView(LoginRequiredMixin, ListView):
    model = CreditCardOffer
    # These next two lines tell the view to index lookups by username
    slug_field = "id"
    slug_url_kwarg = "id"
    paginate_by = 10


class CreditCardOfferAPIListView(generics.ListAPIView):
    serializer_class = CreditCardOfferListSerializer

    def get_queryset(self):
        queryset = CreditCardOffer.objects.all()
        website = self.request.query_params.get('website', None)
        if website is not None:
            queryset = queryset.filter(domain=website)
        return queryset


class MultiSerializerViewSet(viewsets.ModelViewSet):
    serializers = {
        'default': None,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action,
                                    self.serializers['default'])


class CreditCardOfferViewSet(ListCacheResponseMixin, MultiSerializerViewSet):
    queryset = CreditCardOffer.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    serializers = {
        'list':    CreditCardOfferListSerializer,
        'detail':  CreditCardOfferDetailSerializer,
        'default': CreditCardOfferDetailSerializer,
        # etc.
    }
    def get_queryset(self):
        queryset = CreditCardOffer.objects.all().order_by('extracted_fields')
        website = self.request.query_params.get('website', None)
        if website is not None:
            queryset = queryset.filter(domain=website)
        return queryset


class CreditCardWebsiteView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        data = list()
        for row in CreditCardOffer.objects.all().values('domain').annotate(creditcard_count=Count('domain')):
            row['short_domain'] = row['domain'].replace('www.', '')
            data.append(row)
        return Response(data)
