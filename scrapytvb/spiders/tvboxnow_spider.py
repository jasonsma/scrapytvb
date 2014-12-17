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
            xpath = '/html/body[@id="forumdisplay"]/div[@id="wrap"]/div'\
                    '[@class="main"]/div[@class="content"]/table/tbody/tr'\
                    '/td[1]/div[@id="threadlist"]/form[@id="moderate"]'\
                    '/table[@class="datatable"]/tbody/tr/th[@class="subject '\
                    'hot"]/span[@id]/a'
            xpath = "//table[@class='datatable']/tbody[@id]/tr/th[@class='subject hot']/span[@id]/a/text()"
            # example selected
            sel = Selector(response)
            lines = sel.xpath(xpath).extract()
            for l in lines:
                l.encode('utf-8')
                print l
            #print sel.xpath(xpath).extract()
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


