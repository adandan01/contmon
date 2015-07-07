import csv
from datetime import datetime
import time
from optparse import OptionParser
import urlparse
import os
from PIL import Image
import cStringIO
import base64
import hashlib

from selenium.common.exceptions import NoSuchElementException
import simplejson
from selenium import webdriver

try:
    from xvfbwrapper import Xvfb
except ImportError:
    Xvfb = None

EXTRACTOR_STYLE_CSS = 'css'
EXTRACTOR_STYLE_XPATH = 'xpath'

## Save a screenshot of the current page.
def take_screenshot(driver, name, save_location):
    # Make sure the path exists.
    path = os.path.abspath(save_location)
    if not os.path.exists(path):
        os.makedirs(path)
    full_path = '%s/%s' % (path, name)
    driver.save_screenshot(full_path)
    return full_path


def press_enter():
    from os import system

    keys = 'return'
    system('osascript -e \'tell application "System Events" to keystroke ' + keys + "'")


def save_page_source(name, save_location):
    # Make sure the path exists.
    path = os.path.abspath(save_location)
    if not os.path.exists(path):
        os.makedirs(path)
    full_path = '%s/%s' % (path, name)
    content = driver.page_source
    with open(full_path, "w") as text_file:
        text_file.write(content)
    return content


def save_extraction_result(save_location, name, results):
    # Make sure the path exists.
    path = os.path.abspath(save_location)
    if not os.path.exists(path):
        os.makedirs(path)
    full_path = '%s/%s' % (path, name)
    with open(full_path, "w") as text_file:
        text_file.write(simplejson.dumps(results))
    return full_path


def extract_elements(extractor, extractor_style):
    if extractor_style == EXTRACTOR_STYLE_CSS:
        elements = driver.find_elements_by_css_selector(extractor)
    elif extractor_style == EXTRACTOR_STYLE_XPATH:
        elements = driver.find_elements_by_xpath(extractor)
    filter_elements = [e for e in elements if e.location['x'] and e.location['y']]
    print 'find elements', len(elements), 'fitlered', len(filter_elements)
    return filter_elements


def extract_url(url, extractor, extractor_style='css', next_page_selector=None, tab_selector=None, base_dir=None):
    print 'crawling url ', url
    driver.get(url)
    print 'done crawling url ', url
    parsed_url = urlparse.urlparse(url)
    page_source = '%s_%s.html' % (parsed_url.hostname, parsed_url.path.split('/')[-1])
    raw_html = save_page_source(page_source, base_dir)

    print "Page souce save to %s" % page_source

    elements = extract_elements(extractor, extractor_style)
    results = list()
    i = 1
    screenshots = list()
    next_element = True
    if tab_selector:
        tabs = driver.find_elements_by_css_selector(tab_selector)
    else:
        tabs = None

    if tabs and len(tabs) > 0:

        print 'found tabs: ', len(tabs)
        for tab in tabs:

            tab.click()
            elements = extract_elements(extractor, extractor_style)
            screenshot = take_screenshot(driver,
                                         '%s_%s_%d.png' % (parsed_url.hostname, parsed_url.path.split('/')[-1], i),
                                         base_dir)

            print "Screenshot saved to: %s" % screenshot
            img = Image.open(screenshot)
            jpeg_image_buffer = cStringIO.StringIO()
            img.save(jpeg_image_buffer, format="png", quality=100, optimize=True, progressive=True)
            img_str = base64.b64encode(jpeg_image_buffer.getvalue())
            screenshots.append(img_str)

            for j, element in enumerate(elements):
                location = element.location
                size = element.size

                if size['width'] and size['height']:
                    extracted_result = {'text': element.text, 'size': size, 'location': location, 'html': element.get_attribute('outerHTML'),
                                        'content_hash': hashlib.md5(element.text).hexdigest(), 'page_num': i}
                    #print 'html', extracted_result['html']
                    results.append(extracted_result)

            i += 1
    else:

        while next_element:
            screenshot = take_screenshot(driver,
                                         '%s_%s_%d.png' % (parsed_url.hostname, parsed_url.path.split('/')[-1], i),
                                         base_dir)

            print "Screenshot saved to: %s" % screenshot
            img = Image.open(screenshot)
            jpeg_image_buffer = cStringIO.StringIO()
            img.save(jpeg_image_buffer, format="png", quality=100, optimize=True, progressive=True)
            img_str = base64.b64encode(jpeg_image_buffer.getvalue())
            screenshots.append(img_str)

            for j, element in enumerate(elements):
                location = element.location
                size = element.size

                if size['width'] and size['height']:
                    extracted_result = {'text': element.text, 'size': size, 'location': location, 'html': element.get_attribute('outerHTML'),
                                        'content_hash': hashlib.md5(element.text).hexdigest(), 'page_num': i}

                    results.append(extracted_result)

            i += 1

            if next_page_selector:

                try:
                    next_element = driver.find_element_by_css_selector(next_page_selector)
                    if next_element:
                        if next_element.get_attribute("disabled"):
                            print ' next element is disabled'
                            break
                        else:
                            print 'clicking next page', next_element.get_attribute("disabled")
                            next_element.click()
                            time.sleep(0.3)
                            elements = extract_elements(extractor, extractor_style)
                except NoSuchElementException:
                    print 'no next element'
                    next_element = None

            else:
                print 'nothing to click next page'
                break
                # Click next
                # extract again

    return {'url': url,
            'results': results, 'extractor_style': extractor_style, 'extractor': extractor,
            'crawled_on': str(
                datetime.now().isoformat()), 'screenshots': screenshots}  # 'raw_html': raw_html,


fp = webdriver.FirefoxProfile()

fp.set_preference("browser.download.folderList", 2)
fp.set_preference("browser.download.manager.showWhenStarting", False)
fp.set_preference("browser.download.dir", '/vagrant_data/screenshots')
# fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
fp.set_preference("browser.helperApps.neverAsk.saveToDisk",
                  "text/html, application/xhtml+xml, application/xml, application/csv, text/plain, application/vnd.ms-excel, text/csv, text/comma-separated-values, application/octet-stream")
fp.set_preference("browser.helperApps.alwaysAsk.force", False)
# fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")
# fp.add_extension(extension='/vagrant_data/unmht-7.3.0.5-sm+an+fx+tb.xpi')
# fp.set_preference("extensions.unmht.currentVersion", "7.3.0.5")  #Avoid startup screen
fp.set_preference('extensions.unmht.shortcut.save.quick', True)

parser = OptionParser()
parser.set_defaults(url='')
parser.set_defaults(input='')

parser.add_option("-u", "--url", type="string", help="url")
parser.add_option("-i", "--input", type="string", help="input list")
parser.add_option("-d", "--domain", type="string", help="input list")

(options, args) = parser.parse_args()

if Xvfb:
    xvfb = Xvfb(width=1280, height=720)
    xvfb.start()
driver = webdriver.Firefox(firefox_profile=fp)
# driver = webdriver.Firefox()
driver.set_window_size(1280, 720)

scraper_config = {
    'www.bankrate.com': {'style': 'css', 'extractor': '.br-rate-table-row', 'next_page_selector': ".nextPage", 'input_file': 'bankrate_urls.txt'},  # done
    'www.creditkarma.com': {'style': 'css', 'extractor': 'div[ck-card]', 'tab_selector': 'a[ck-tab]',
                            'next_page_selector': None, 'input_file': 'creditkarma_urls.txt', 'protocol': 'https'},
    'www.cardhub.com': {'style': 'css', 'extractor': '.card', 'next_page_selector': '.next', 'input_file': 'cardhub_urls.txt', 'protocol':'https'},  # done

    'www.123apply.com': {'style': 'xpath', 'next_page_selector': None, 'input_file': '123apply_urls.txt',
                         'extractor': '/html/body/table[2]/tbody/tr/td[2]/table[descendant::*[contains(@class, "insidecard")]]'},
}

url = options.url
domain = options.domain

urls = list()
if url:
    urls.append(url)
elif domain and domain in scraper_config:
    input = scraper_config[domain]['input_file']
    protocol = scraper_config[domain].get('protocol', 'http')
    with open(input, 'rb') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            url = row['URL']
            print url, 'domain', domain
            urls.append(protocol + "://" + domain + url)

else:
    with open(options.input, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            urls.append(row[1])

print 'crawling %d urls' % len(urls)

# TODO: read input from a file and remember to pause

for url in urls:
    parsed_url = urlparse.urlparse(url)
    print url
    base_dir = '/vagrant/contmon/data/scraper/' + '%s_%s/' % (
        parsed_url.hostname, parsed_url.path.split('/')[-1])
    extractor = scraper_config[parsed_url.netloc]
    result = extract_url(url, extractor['extractor'],
                         extractor['style'], extractor.get('next_page_selector', None),
                         extractor.get('tab_selector', None), base_dir)
    save_extraction_result(base_dir, '%s_%s.json' % (parsed_url.hostname, parsed_url.path.split('/')[-1]),
                           result)

driver.quit()

if Xvfb:
    xvfb.stop()
