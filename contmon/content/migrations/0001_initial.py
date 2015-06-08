# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CrawledPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_number', models.IntegerField()),
                ('image', models.ImageField(upload_to=b'')),
                ('text', models.TextField(blank=True)),
                ('content_hash', models.CharField(max_length=500, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='CrawlUrl',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.CharField(max_length=500, db_index=True)),
                ('domain', models.CharField(max_length=400, db_index=True)),
                ('path', models.CharField(max_length=400)),
                ('crawled_on', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='CreditCardOffer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.CharField(default=b'', max_length=400, db_index=True)),
                ('image', models.ImageField(upload_to=b'')),
                ('location_x', models.FloatField()),
                ('location_y', models.FloatField()),
                ('size_width', models.FloatField()),
                ('size_height', models.FloatField()),
                ('content_hash', models.CharField(max_length=500, db_index=True)),
                ('text', models.TextField(blank=True)),
                ('crawl_urls', models.ManyToManyField(to='content.CrawlUrl')),
            ],
            options={
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
