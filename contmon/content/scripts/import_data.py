import glob
import urlparse
from PIL import Image
import cStringIO
import base64
from io import BytesIO

from django.core.files.base import ContentFile

from bvgs.serialization.json import load_data_from_json_file
from contmon.content.models import CrawlUrl, CrawledPage, CreditCardOffer


def run():
    file_paths = glob.glob('/home/brandverity/contmon/data/**/*.json')
    print 'importing data from contmon'
    for data_file in file_paths:
        print 'reading from', data_file
        page_result = load_data_from_json_file(data_file)
        parsed_url = urlparse.urlparse(page_result['url'])
        domain = parsed_url.netloc
        path = parsed_url.path

        print page_result.keys()
        crawled_pages = list()
        # saving full crawled pages
        crawl_url = None
        for i, screenshot_str in enumerate(page_result['screenshots']):
            page_num = i + 1
            img = Image.open(cStringIO.StringIO(base64.b64decode(screenshot_str)))

            doc = {'id': page_result['url'] + ' ' + str(page_num), 'url': page_result['url'], 'domain': domain,
                   'path': path, 'page_num': page_num,
                   'img_base_64': screenshot_str,
                   'crawled_on': page_result['crawled_on']}
            print 'indexing doc', doc['id']
            if crawl_url is None:
                crawl_url, created = CrawlUrl.objects.get_or_create(url=page_result['url'], path=path, domain=domain)
            # TODO: create a method that wraps this on the manager
            crawled_page, created = CrawledPage.objects.get_or_create(crawl_url=crawl_url, page_number=page_num,
                                                                      content_hash="",
                                                                      text="")

            crawled_page.image.save( domain + '_' + path + '_page_' + str(page_num) + ".png",
                                    ContentFile(base64.b64decode(screenshot_str)))
            crawled_pages.append({'crawled_page': crawled_page, 'image': img})

        print 'finishing indexing full crawled pages. number of screenshots: ', len(page_result['screenshots'])

        for j, row in enumerate(page_result['results']):
            crawled_page = crawled_pages[row['page_num'] - 1]
            row['title'] = row['text'].split('\n')[0]
            row['url_and_page_num'] = {'url': page_result['url'], 'page_num': row['page_num']}
            row['domain'] = domain
            row['path'] = path
            a = path.split('/')[-1].split('-')
            category = ' '.join(a[:-1])
            row['category'] = category
            location = row['location']
            size = row['size']
            # TODO: create a method that wraps this on the manager
            # TODO: check if offer with the same hash exist.
            # if it does, offer can happen on many different urls.
            # a url has many offers
            try:

                offer = CreditCardOffer.objects.get(domain=crawled_page['crawled_page'].crawl_url.domain,
                                                    content_hash=row['content_hash'])
            except CreditCardOffer.DoesNotExist:
                offer = CreditCardOffer.objects.create(domain=crawled_page['crawled_page'].crawl_url.domain,
                                                       content_hash=row['content_hash'], location_x=location['x'],
                                                       location_y=location['y'], size_width=size['width'],
                                                       size_height=size['height'], text=row['text'])
                with BytesIO() as file_buffer:
                    left = location['x']
                    top = location['y']
                    right = location['x'] + size['width']
                    bottom = location['y'] + size['height']
                    print 'saving img', location, size
                    img = crawled_page['image']
                    new_image = img.crop((left, top, right, bottom))  # defines crop points
                    new_image.save(file_buffer, format="png", quality=100, optimize=True, progressive=True)
                    #TODO: improve file name to be more sensible
                    offer.image.save(
                        '_'.join([crawled_page['crawled_page'].crawl_url.domain, row['path'], str(row['page_num']), str(j),'png']),
                        ContentFile(file_buffer.getvalue()))

            # offer was found on this page
            offer.crawl_urls.add(crawl_url)
