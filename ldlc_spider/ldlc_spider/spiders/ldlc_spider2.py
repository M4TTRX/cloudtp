from urllib.parse import urlencode

import scrapy
import datetime


class QuotesSpider(scrapy.Spider):
    name = "ldlc2"
    start_urls = [
        'https://www.ldlc.com/products_sitemap.xml',
    ]
    # user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 " \
    # "Safari/537.1"
    # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 "

    BASE_URL = 'https://www.ldlc.com'

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    def get_price(self, response) -> float:
        try:
            euros = float(response.css('div.price div.price::text').get()[:-1])
            cents = float(response.css('div.price div.price sup::text').get())
            return euros + cents * 0.01
        except:
            return -1

    def get_stock(self, response) -> str:

        # stock is based on an enum that is sotred in the data-stock-web 
        # attribute of the div.modal-stock-web.pointer.stock element
        stock_type = response.css('div.modal-stock-web.pointer.stock::attr(data-stock-web)').get()
        if stock_type == '1':
            return 'IN STOCK'
        if stock_type == '2':
            return 'IN STOCK'
        if stock_type == '4':
            return 'IN STOCK IN UNDER 7 DAYS'
        if stock_type == '5':
            return 'IN STOCK IN 7 TO 15 DAYS'
        if stock_type == '6':
            return 'IN STOCK IN 15+ DAYS'
        if stock_type == '9':
            return 'OUT OF STOCK'
        self.log('Unknown stock type for product: ' + response.url)
        return 'UNKNOWN'

    def get_reviews(self, response) -> int:
        try:
            return int(response.css('div.average em::text')[1].get()[4:-5])
        except:
            return 0

    def get_rating(self, response) -> int:
        try:
            return int(response.css('div.note::text').get())
        except:
            return 0

    def get_categories(self, response) -> dict:
        categories = response.css('div.breadcrumb ul li')
        categories_dict = {}
        for i in range(1, len(categories), 2):
            categories_dict[f'category_{(i - 1) >> 1}'] = {
                'name': categories[i].css('a::text').get()[29:-25],
                'url': self.BASE_URL + categories[i].css('a::attr(href)').get()
            }
        return categories_dict

    def parse(self, response):
        # explore all products from the product sitemap
        if type(response) is scrapy.http.response.xml.XmlResponse:
            response.selector.remove_namespaces()
            products_urls = response.xpath('url/loc/text()').getall()
            products_number = len(products_urls) // 3
            products = [url for url in products_urls[products_number:(
                        2 * products_number)]]  # one third of products for the first spider
            yield from response.follow_all(products, headers=self.HEADERS, callback=self.parse)
        yield {
            'title': response.css('title::text').get(),
            'datetime': datetime.datetime.now(),
            'url': response.url,
            'description': response.css('p.desc::text').get(),
            'image': response.css('div.product a img::attr(src)').get(),
            'price': self.get_price(response),

            # stock is based on an enum that is sotred in the data-stock-webs
            'stock': self.get_stock(response),

            # rating score out of 10 (because rating uses half stars), and number of reviews
            'rating': self.get_rating(response),
            'reviews': self.get_reviews(response),

            # categories of the product starting with more general categories and going towards sub categories
            # example: category_0 will be something vague like 'Computer' and category_1 will be something more specific like 'Computer Case'
            'categories': self.get_categories(response)
        }
