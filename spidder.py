from crapy.contrib.spiders import CrawlSpider
class MySpider(CrawlSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com']

    rules = (
        # Extract and follow all links!
        Rule(LinkExtractor(callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        self.log('crawling'.format(response.url))