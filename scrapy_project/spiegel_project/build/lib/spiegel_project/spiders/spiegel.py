# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor


class SpiegelSpider(scrapy.Spider):
    name = "spiegel"
    start_urls = [
        'http://www.spiegel.de/politik/',
    ]


    rules = (
        Rule(LxmlLinkExtractor(allow_domains='spiegel.de/')),
    )

    def parse(self, response):
        """
        Standard callback for every URL in @start_urls
        Extracts all Article URL from a spiegel.de rubric page
        Only fetches subdomains of @start_urls
        :param response:  a spiegel.de rubric page e.g. 'http://www.spiegel.de/politik/'
        :return: parsed articles 
        """
        # extracts Urls within the given start_url
        for link in LxmlLinkExtractor(allow=map(lambda x: x+'[a-z]+/.+html', self.start_urls)).extract_links(response):
            yield response.follow(link.url, callback=self.parse_article)
        # extracts the archive link on the current page and parses its content recursivly
        for archive_link in LxmlLinkExtractor(allow=map(lambda x: x+'archiv.*.html', self.start_urls)).extract_links(response):
            yield response.follow(archive_link.url)


    def parse_article(self, response):
        """
        Parsing of a single article 
        :param response: The whole article as an HTML object
        :return: Article as a datapoint 
        """
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