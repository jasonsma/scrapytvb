from scrapy.spider import BaseSpider
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector

from scrapytvb.items import Forum81Item

class LoginSpider(BaseSpider):
    name = 'tvboxnow'
    allowed_domains = ['tvboxnow.com']
    start_urls = ['http://www.tvboxnow.com/logging.php?action=login']

    def parse(self, response):
        if 'tvbgetter' in response.body:
            self.log("Successful login. Time to crawl.")
            open('forum-8-1', 'wb').write(response.body)
            #xpath_row = "//table[@class='datatable']/tbody[@id]/tr"
            #xpath_title = "//table[@class='datatable']/tbody[@id]/tr/th[@class='subject hot']/span[@id]/a/text()"
            #xpath_author ="//table[@class='datatable']/tbody[@id]/tr/td[@class='author']/cite/a/text()"
            #xpath_date = "//table[@class='datatable']/tbody[@id]/tr/td[@class='author']/em"

            entries = response.xpath("//table[@class='datatable']/tbody[@id]/tr")
            for entry in entries:
                title = entry.xpath("th[@class='subject hot']/span[@id]/a/text()").extract()
                author = entry.xpath("td[@class='author']/cite/a/text()").extract()
                date = entry.xpath("td[@class='author']/em/text()").extract()
                link = entry.xpath("th[@class='subject hot']/span[@id]/a/@href").extract()
                if title and author and date:
                    title[0].encode('utf-8')
                    print title[0], author[0], date[0], link[0]

            return None
        else:
            return [FormRequest.from_response(response,
                    formdata={'username': 'tvbgetter', 'password': 'abc123'},
                    callback=self.after_login)]

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.log("Login failed", level=log.ERROR)
            return

        # continue scraping with authenticated session...
        # returning this Request without a callback goes back to parsed
        return Request('http://www.tvboxnow.com/forum-8-1.html')


