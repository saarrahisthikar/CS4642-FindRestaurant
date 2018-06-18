import scrapy


class FindRestaurant(scrapy.Spider):
    name = "restaurant"
    start_urls = [
        'http://www.tasty.lk/restaurants',
    ]

    def parse(self, response):

        # follow links to restaurant information pages
        for href in response.css('div.media-body a::attr(href)'):
            yield response.follow(href, self.parse_restaurant)

        # follow paginatioon links
        for href in response.css('div.pagination-info-bottom a[rel="next"]::attr(href)'):
            yield response.follow(href, self.parse)

    def parse_restaurant(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first()

        yield{
            'name': extract_with_css('#rest-title::text'),
            'address': extract_with_css('div.panel-heading span.address span::text'),
            'servicing_cuisines': response.css('div.panel-body p.cuisine span::text').extract(),
            'open_hours': extract_with_css('#openHours::text'),
            'price_range': extract_with_css('div.panel-body p.price-range span::text'),
            'near_by_restaurants': response.css('#nearbyList li.media a::text')[:-1].extract(),
        }

