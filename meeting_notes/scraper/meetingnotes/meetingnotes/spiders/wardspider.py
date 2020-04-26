# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from meetingnotes.items import MeetingNotesItem

from meetingnotes import get_id_from_google_drive_url, download_google_drive_file


class WardspiderSpider(CrawlSpider):
    name = 'wardspider'
    allowed_domains = ['www.dropbox.com', 'drive.google.com/'
        'anc1a.org/minutes/', 'www.anc1b.org']
    start_urls = [
        'http://anc1a.org/minutes/', # Works
        # 'https://www.anc1b.org/new-page-2'
    ]

    rules = (
        # Rule(LinkExtractor(allow=r'drive.google.com/'), callback='parse_google_doc_link', follow=True),
        # Rule(LinkExtractor(allow=r'www.dropbox.com'), callback='parse_pdf_doc_link', follow=True),
        Rule(LinkExtractor(allow='minutes'), callback='parse', follow=True),
    )

    def parse(self, response):
        for l in LinkExtractor(allow=r'drive.google').extract_links(response):
            it = MeetingNotesItem()
            it['ward'] = re.search('\d[a-z]', response.url.split('.')[-2])[0]
            it['link'] = l.url
            it['text'] = l.text
            yield it


    def parse_pdf_doc_link(self, response):
        self.logger.warning("test pdf parse")

        item = MeetingNotesItem()
        item['ward'] = re.search('\d[a-z]', response.url.split('.')[-2])[0]
        return item