import scrapy
import datetime
class QuotesSpider(scrapy.Spider):

    name = "ldlc"
    start_urls = [
        'https://www.ldlc.com/products_sitemap.xml',
    ]
    
    BASE_URL = 'https://www.ldlc.com'
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
        match stock_type:
            case '1':
                return 'IN STOCK'
            case '2':
                return 'IN STOCK'
            case '4':
                return 'IN STOCK IN UNDER 7 DAYS'
            case '5':
                return 'IN STOCK IN 7 TO 15 DAYS'
            case '6':
                return 'IN STOCK IN 15+ DAYS'
            case '9':
                return 'OUT OF STOCK'
            case _:
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
            categories_dict[f'category_{(i-1)>>1}'] = {
                'name': categories[i].css('a::text').get()[29:-25],
                'url': self.BASE_URL + categories[i].css('a::attr(href)').get()
            }
        return categories_dict
            
    def parse(self, response):
        
        # explore all products from the product sitemap
        if type(response) is scrapy.http.response.xml.XmlResponse:
            response.selector.remove_namespaces()
            products = response.xpath('//url/loc/text()')[:40]
            yield from response.follow_all(products, callback=self.parse)
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