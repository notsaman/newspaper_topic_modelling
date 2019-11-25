# -*- coding: utf-8 -*-
import string

import scrapy
from lxml import html


class SpiegelSpider(scrapy.Spider):
    """
    Crawls a single spiegel.de article             
    """
    name = "spiegel-single"
    start_urls = [
        # 'http://www.spiegel.de/politik/deutschland/kommentar-wie-sich-die-gruenen-ins-abseits-streiten-a-1148700.html',
        'http://www.spiegel.de/politik/ausland/mohammed-karikaturen-in-daenemark-wie-es-den-machern-heute-geht-a-1141686.html',
        # plus
    ]

    # extracting article content through links on the rubric page
    # parse will we called for the elements of start_url (default callback)
    def parse(self, response):
        article_column = response.xpath('//*[@id="js-article-column"]/div')
        intro_p = response.xpath('//p[@class="article-intro"]')
        author_p = response.xpath('//p[@class="author"]')

        # Fixes issues with missing text from highlighted words
        tree = html.fromstring("".join(article_column.xpath('./p').extract()))
        text = tree.text_content().strip()

        # Spiegel Plus extraction
        obfuscated = article_column.xpath('//div[@class="obfuscated-content"]')
        if obfuscated.extract_first() is not None:
            tree_obfus = html.fromstring("".join(obfuscated.xpath('./p[@class="obfuscated"]').extract()))
            obfuscated_text = tree_obfus.text_content().strip()
            decrypted_text = "".join(map(lambda c: chr(ord(c)-1) if c not in ' ' else c, obfuscated_text))
        else:
            decrypted_text = ""

        yield {
            'rubric': response.xpath('//*[@id="header"]/div[2]/div[1]/a/text()').extract_first(),
            'timestamp': article_column.xpath('./div[2]/span/time/attribute::datetime').extract_first(),
            'author': author_p.xpath('./a/text()').extract(),
            'source': response.xpath('//*[@id="js-article-column"]/p/i/text()').extract_first(),
            # 'headline': response.xpath('//*[@id="content-main"]/div[1]/div[3]/h2/span[2]/text()').extract_first(),
            # 'intro': intro_p.xpath('./strong/text()').extract_first(),
            'text': text,
            'plus_text': decrypted_text
            # 'text': "".join(article_column.xpath('./p/text()').extract())
        }
