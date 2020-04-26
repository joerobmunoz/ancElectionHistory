import scrapy as sc
from scrapy.selector import Selector

import bs4, re
import markdown as md
import gdown


# f = open('data.md', 'r')

# hmd = md.markdown( f.read() )

# uri_pattern = re.compile('^http*')
# soup = bs4.BeautifulSoup(hmd)
# ward_root_uris = soup.findAll(text=uri_pattern)


def get_ward_num_from_ward_uri(uri_node):
    ward_letter = re.search("<li>([a-zA-Z])<ul>*", str(uri_node.parent.parent.parent)).group(1)
    ward_num = re.search("([0-9])</p>", str(uri_node.parent.parent.parent.parent.parent)).group(1)
    return ward_letter, ward_num

class WardMeetingNotesSpider(sc.Spider):
    name = "brickset_spider"
    start_urls = [ward_root_uris[0]]
    
    def parse(self, response):            
        # Patterns for traversing pages
            # month <a> links (e.g. jan|feb|)
            
        s = Selector(response=response)
        anchors = response.css('a').xpath('@href').extract()
        
        yield parse_for_pdf(anchors)
        
        # Crawl more
        
#         month_re = re.compile(r'(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)', re.IGNORECASE)
#         month_links = filter(month_re.match, anchors)
#         NEXT_PAGE_SELECTOR = 'a ::attr(href)'
#         next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
#         if next_page:
#             yield scrapy.Request(
#                 response.urljoin(next_page),
#                 callback=self.parse
#             )

    def parse_for_downloads(self, anchors):
        gdrive_p = r'drive\.google\.com'
        pdf_p = r'|\.pdf|'
    
        for gdrive_link in re.findall(gdrive_p, anchors):
            yield Request(
                url=response.urljoin(gdrive_link),
                callback=self.save_gdrive_pdf
            )
            
#         for pdf_link in re.findall(pdf_p, anchors):
#             yield Request(
#                 url=response.urljoin(pdf_link),
#                 callback=self.save_pdf
#             )

    def save_gdrive_pdf(self, response):
        path = response.url.split('/')[-1]
        gdown.download(response.url, path, quiet=False) 


    def save_pdf(self, response):
        path = response.url.split('/')[-1]
        self.logger.info('Saving PDF %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)

from scrapy.crawler import CrawlerRunner
process = CrawlerRunner({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
process.crawl(WardMeetingNotesSpider)
# process.start()