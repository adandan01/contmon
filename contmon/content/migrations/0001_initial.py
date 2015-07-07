# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrawledPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('page_number', models.IntegerField()),
                ('image', models.ImageField(upload_to=b'crawled_page')),
                ('text', models.TextField(blank=True)),
                ('content_hash', models.CharField(max_length=500, db_index=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CrawlUrl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('url', models.CharField(max_length=500, db_index=True)),
                ('domain', models.CharField(max_length=400, db_index=True)),
                ('path', models.CharField(max_length=400)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CreditCardOffer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('domain', models.CharField(default=b'', max_length=400, db_index=True)),
                ('image', models.ImageField(upload_to=b'extracted_content')),
                ('html', models.FileField(upload_to=b'html')),
                ('extracted_fields', jsonfield.fields.JSONField()),
                ('location_x', models.FloatField()),
                ('location_y', models.FloatField()),
                ('size_width', models.FloatField()),
                ('size_height', models.FloatField()),
                ('content_hash', models.CharField(max_length=500, db_index=True)),
                ('text', models.TextField(blank=True)),
                ('review_state', models.SmallIntegerField(default=0, db_index=True, choices=[(0, b'Never Reviewed'), (1, b'Compliant'), (2, b'Not Compliant'), (3, b'Irrelevant: Ignore')])),
                ('crawl_urls', models.ManyToManyField(to='content.CrawlUrl')),
            ],
            options={
                'ordering': ['extracted_fields'],
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='crawledpage',
            name='crawl_url',
            field=models.ForeignKey(to='content.CrawlUrl'),
        ),
        migrations.AlterUniqueTogether(
            name='creditcardoffer',
            unique_together=set([('domain', 'content_hash')]),
        ),
    ]
