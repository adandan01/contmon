# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    replaces = [('scraper', '0001_initial'), ('scraper', '0002_auto_20150706_2105'), ('scraper', '0003_auto_20150706_2108'), ('scraper', '0004_auto_20150706_2110'), ('scraper', '0005_auto_20150706_2116')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WebsiteScraperConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('domain', models.CharField(max_length=400, db_index=True)),
                ('selector_style', models.CharField(blank=True, max_length=100, choices=[(b'css', b'css'), (b'xpath', b'xpath')])),
                ('name_selector', models.CharField(max_length=100, blank=True)),
                ('image_selector', models.CharField(max_length=100, blank=True)),
                ('content_selector', models.CharField(max_length=100)),
                ('next_page_selector', models.CharField(max_length=100, blank=True)),
                ('tabs_selector', models.CharField(max_length=100, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
