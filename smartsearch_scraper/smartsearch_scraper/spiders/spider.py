import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

class SmartSearchCrawler(CrawlSpider):
    name = 'smartsearch_crawler'
    allowed_domains = []  
    start_urls = []

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'AUTOTHROTTLE_ENABLED': True,
        'ROBOTSTXT_OBEY': True,
        'DEPTH_LIMIT': 3,
        'RETRY_TIMES': 3,
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output/advanced_output.json'
    }

    rules = (
        Rule(
            LinkExtractor(),
            callback='parse_item',
            follow=True
        ),
    )

    def __init__(self, *args, **kwargs):
        super(SmartSearchCrawler, self).__init__(*args, **kwargs)

        # Read URLs dynamically from a text file
        with open('start_urls.txt', 'r') as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]
            self.start_urls = urls

        # Automatically infer allowed domains
        domains = set()
        for url in self.start_urls:
            domain = url.split("//")[-1].split("/")[0]
            domains.add(domain)
        self.allowed_domains = list(domains)

    def parse_item(self, response):
        title = response.css('title::text').get()
        headings = response.css('h1::text, h2::text, h3::text').getall()
        paragraphs = response.css('p::text').getall()
        meta_description = response.xpath("//meta[@name='description']/@content").get()

        yield {
            'url': response.url,
            'title': title,
            'headings': headings,
            'paragraphs': paragraphs,
            'meta_description': meta_description,
        }