# -*- coding: utf-8 -*-
import scrapy
from lxml import html
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Rule


class SpiegelSpider(scrapy.Spider):
    name = "spiegel"

    start_urls = [
        # current scrape
        'http://www.spiegel.de/gesundheit/'

        # Done
        # 'http://www.spiegel.de/lebenundlernen/' complete 15k
        # 'http://www.spiegel.de/auto/'          ~14k
        # 'http://www.spiegel.de/reise/'         complete ~20k
        # 'http://www.spiegel.de/gesundheit/'    complete ~5k http 500
        # 'http://www.spiegel.de/wissenschaft/'  complete ~29k
        # 'http://www.spiegel.de/netzwelt/'      complete ~29k
        # 'http://www.spiegel.de/kultur/'       ~35k
        # 'http://www.spiegel.de/panorama/'     ~35k
        # 'http://www.spiegel.de/wirtschaft/'   ~35k
        # 'http://www.spiegel.de/politik/',     ~35k
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
        denied_url = ".*nachrichten-am-morgen-die-news.*"
        allowed_url = "".join(map(lambda x: x + '[a-z]+/.+html', self.start_urls))
        archive_rgx = "".join(map(lambda x: x + 'archiv.*.html', self.start_urls))

        for link in LxmlLinkExtractor(allow=allowed_url, deny=denied_url).extract_links(response):
            yield response.follow(link.url, callback=self.parse_article)

        # extracts the archive link on the current page and parses its content recursivly
        for archive_link in LxmlLinkExtractor(allow=archive_rgx).extract_links(
                response):
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

        # Fixes issues with missing text from highlighted words
        tree = html.fromstring("".join(article_column.xpath('./p').extract()))
        text = tree.text_content().strip()

        # Spiegel Plus extraction
        obfuscated = article_column.xpath('//div[@class="obfuscated-content"]')
        decrypted_text = ""
        if obfuscated.extract_first() is not None:
            tree_obfus = html.fromstring("".join(obfuscated.xpath('./p[@class="obfuscated"]').extract()))
            obfuscated_text = tree_obfus.text_content().strip()
            decrypted_text = "".join(map(lambda c: chr(ord(c) - 1) if c not in ' ' else c, obfuscated_text))

        yield {
            'rubric': response.xpath('//*[@id="header"]/div[2]/div[1]/a/text()').extract_first(),
            'timestamp': article_column.xpath('./div[2]/span/time/attribute::datetime').extract_first(),
            'author': author_p.xpath('./a/text()').extract(),
            'source': response.xpath('//*[@id="js-article-column"]/p/i/text()').extract_first(),
            'headline': response.xpath('//*[@id="content-main"]/div[1]/div[3]/h2/span[2]/text()').extract_first(),
            'intro': intro_p.xpath('./strong/text()').extract_first(),
            'text': text,
            'plus_text': decrypted_text

        }
