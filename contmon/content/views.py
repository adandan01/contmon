# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from braces.views import LoginRequiredMixin
from rest_framework import viewsets
from .serializers import CreditCardOfferSerializer

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


class CreditCardOfferViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = CreditCardOffer.objects.all()
    serializer_class = CreditCardOfferSerializer

