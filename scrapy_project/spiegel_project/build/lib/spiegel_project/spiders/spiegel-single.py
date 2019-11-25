# -*- coding: utf-8 -*-
import scrapy


class SpiegelSpider(scrapy.Spider):
    """
    Crawls a single spiegel.de article             
    """
    name = "spiegel-single"
    start_urls = [
        'http://www.spiegel.de/politik/deutschland/bundeswehr-der-rechte-kosmos-des-franco-a-a-1147221.html',
    ]

    # extracting article content through links on the rubric page
    # parse will we called for the elements of start_url (default callback)
    def parse(self, response):
        article_column = response.xpath('//*[@id="js-article-column"]/div')
        intro_p = response.xpath('//p[@class="article-intro"]')
        author_p = response.xpath('//p[@class="author"]')

        yield {
            'rubric': response.xpath('//*[@id="header"]/div[2]/div[1]/a/text()').extract_first(),
            'timestamp': article_column.xpath('./div[2]/span/time/attribute::datetime').extract_first(),
            'author': author_p.xpath('./a/text()').extract(),
            'source': response.xpath('//*[@id="js-article-column"]/p/i/text()').extract_first(),
            'headline': response.xpath('//*[@id="content-main"]/div[1]/div[3]/h2/span[2]/text()').extract_first(),
            'intro': intro_p.xpath('./strong/text()').extract_first(),
            'text': "".join(article_column.xpath('./p/text()').extract())
        }

