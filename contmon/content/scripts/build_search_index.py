# build_index.py
import lxml.html
from lxml.cssselect import CSSSelector
import time
import urlparse
import cStringIO
from PIL import Image
import base64

from bvgs.serialization.json import load_data_from_json_file
from bvgs.storage.filesystem import load_data_from_file


FILE_URL = "http://apps.sloanahrens.com/qbox-blog-resources/kaggle-titanic-data/test.csv"

ES_HOST = {
    "host": "localhost",
    "port": 9200
}

INDEX_NAME = 'extractor'
TYPE_NAME = 'extraction_result'

ID_FIELD = 'content_hash'

FULL_PAGE_INDEX_NAME = 'fullpage'
FULL_PAGE_TYPE_NAME = 'fullpage'
FULL_PAGE_ID_FIELD = 'id'

from elasticsearch import Elasticsearch, NotFoundError

import glob

file_paths = glob.glob('data/**/*.json')
# create ES client, create index
es = Elasticsearch(hosts=[ES_HOST])

REBUILD_INDEX = True
# TODO ability to build from scratch
if REBUILD_INDEX:
    if es.indices.exists(INDEX_NAME):
        print("deleting '%s' index..." % (INDEX_NAME))
        res = es.indices.delete(index=INDEX_NAME)
        print(" response: '%s'" % (res))

    request_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "filter": {
                    "stopwords_filter": {
                        "type": "stop",
                        "stopwords": ["http", "https", "ftp", "www"]
                    }
                },
                "analyzer": {

                    "keylower": {
                        "tokenizer": "keyword",
                        "filter": "lowercase"
                    }
                }

            },
        },
        "mappings": {
            TYPE_NAME: {
                'properties': {
                    'id': {'type': 'string', "index": "not_analyzed"},
                    'img_base_64': {'type': 'binary', },
                    # 'urls': {"type": "string", "index_name": "url", "analyzer": "lowercase"},
                    'url_and_page_num': {
                        "properties": {
                            "url": {"type": "string", "analyzer": "keylower"},
                            "page_num": {"type": "integer"}
                        }
                    },
                    'domain': {"type": "string", "analyzer": "keylower"},
                    'path': {'type': 'string', "analyzer": "keylower"},
                    'category': {'type': 'string', "analyzer": "keylower"},
                    'credit_level': {'type': 'string', "analyzer": "keylower"},
                    'annual_fee': {'type': 'string', "analyzer": "keylower"},

                }
            }
        },


    }

    print("creating '%s' index..." % (INDEX_NAME))
    res = es.indices.create(index=INDEX_NAME, body=request_body)
    print(" response: '%s'" % (res))

    if es.indices.exists(FULL_PAGE_INDEX_NAME):
        print("deleting '%s' index..." % (FULL_PAGE_INDEX_NAME))
        res = es.indices.delete(index=FULL_PAGE_INDEX_NAME)
        print(" response: '%s'" % (res))

    request_body = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "analysis": {
                "filter": {
                    "stopwords_filter": {
                        "type": "stop",
                        "stopwords": ["http", "https", "ftp", "www"]
                    }
                },
                "analyzer": {

                    "keylower": {
                        "tokenizer": "keyword",
                        "filter": "lowercase"
                    }
                }

            },
        },
        "mappings": {
            FULL_PAGE_TYPE_NAME: {
                'properties': {
                    'id': {'type': 'string', "analyzer": "keylower"},
                    'img_base_64': {'type': 'binary', },
                    'url': {"type": "string", "analyzer": "keylower"},
                    'domain': {"type": "string", "analyzer": "keylower"},
                    'path': {'type': 'string', "analyzer": "keylower"},
                    'page_num': {'type': 'integer'}

                }
            }
        },
    }
    #
    print("creating '%s' index..." % (FULL_PAGE_INDEX_NAME))
    res = es.indices.create(index=FULL_PAGE_INDEX_NAME, body=request_body)
    print(" response: '%s'" % (res))

time.sleep(10)

for data_file in file_paths:
    print 'reading from', data_file
    page_result = load_data_from_json_file(data_file)
    parsed_url = urlparse.urlparse(page_result['url'])
    domain = parsed_url.netloc
    path = parsed_url.path

    bulk_data = []

    results = []
    print page_result.keys()
    screenshot_images = list()

    html_file = data_file.replace('json', 'html')
    html = load_data_from_file(html_file)
    tree = lxml.html.fromstring(html)
    credit_level_sel = CSSSelector('div.br-rt-creditneeded')
    annual_fee_sel = CSSSelector('div.br-rt-annualfee')
    credit_levels = credit_level_sel(tree)
    annual_fees = annual_fee_sel(tree)
    for i, screenshot_str in enumerate(page_result['screenshots']):
        page_num = i + 1
        img = Image.open(cStringIO.StringIO(base64.b64decode(screenshot_str)))
        screenshot_images.append(img)
        doc = {'id': page_result['url'] + ' ' + str(page_num), 'url': page_result['url'], 'domain': domain,
               'path': path, 'page_num': page_num,
               'img_base_64': screenshot_str,
               'crawled_on': page_result['crawled_on']}
        res = es.index(index=FULL_PAGE_INDEX_NAME, doc_type=FULL_PAGE_TYPE_NAME, id=doc[FULL_PAGE_ID_FIELD], body=doc)
    print 'finishing reading/indexing images: ', len(screenshot_images)

    for row in page_result['results']:
        row['title'] = row['text'].split('\n')[0]
        row['url_and_page_num'] = {'url': page_result['url'], 'page_num': row['page_num']}
        row['domain'] = domain
        row['path'] = path
        a = path.split('/')[-1].split('-')
        category = ' '.join(a[:-1])
        row['category'] = category
        row['credit_level'] = credit_levels[i].text_content().strip()
        row['annual_fee'] = annual_fees[i].text_content().strip()

        img = screenshot_images[row['page_num'] - 1]
        location = row['location']
        size = row['size']
        left = location['x']
        top = location['y']

        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        #print 'saving img', location, size
        new_image = img.crop((left, top, right, bottom))  # defines crop points

        jpeg_image_buffer = cStringIO.StringIO()
        new_image.save(jpeg_image_buffer, format="jpeg", quality=100, optimize=True, progressive=True)
        row['img_base_64'] = base64.b64encode(jpeg_image_buffer.getvalue())
        # print 'row', row
        op_dict = {
            "index": {
                "_index": INDEX_NAME,
                "_type": TYPE_NAME,
                "_id": row[ID_FIELD]
            }
        }
        # bulk_data.append(op_dict)
        bulk_data.append(row)




    # bulk index the data
    print("indexing...")
    for doc in bulk_data:
        existing = None
        try:
            existing_doc = es.get(index=INDEX_NAME, doc_type=TYPE_NAME, id=doc[ID_FIELD])
            existing = existing_doc['_source']
        except NotFoundError:
            existing = None

        if existing is None:
            existing = doc
            existing['url_and_page_num'] = [doc['url_and_page_num']]
            existing['category'] = [doc['category']]
        else:
            existing['category'].append(doc['category'])

        existing.pop('url', None)
        assert existing.get('url_and_page_num')

        res = es.index(index=INDEX_NAME, doc_type=TYPE_NAME, id=doc[ID_FIELD], body=existing)

    print 'done indexing'
    # print(" response: '%s'" % (res))


# sanity check
print("searching...")
res = es.search(index=INDEX_NAME, size=2, body={"query": {"match_all": {}}})
# print(" response: '%s'" % (res))
print('done searing')

# print("results:")
# for hit in res['hits']['hits']:
# print(hit["_source"])
