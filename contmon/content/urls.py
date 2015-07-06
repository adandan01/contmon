# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'creditcards', views.CreditCardOfferViewSet)

urlpatterns = [
    url(regex=r'^pages/$', view=views.CrawledPageListView.as_view(), name='page-list'),
    url(regex=r'^pages/(?P<id>[\d]+)/$', view=views.CrawledPageDetailView.as_view(), name='page-detail'),
    url(regex=r'^creditcards/$', view=views.CreditCardOfferListView.as_view(), name='creditcard-list'),
    url(regex=r'^creditcards/(?P<id>[\d]+)/$', view=views.CreditCardOfferDetailView.as_view(),
        name='creditcard-detail'),
    url(r'^search/', include('haystack.urls')),
    # url(r'^api/creditcards/$', view=views.CreditCardOfferAPIListView.as_view(), name='creditcard-api-list'),
    url(r'^api/', include(router.urls)),
    url(r'^api/websites/$', view=views.CreditCardWebsiteView.as_view(), name='website-api-list'),
]
