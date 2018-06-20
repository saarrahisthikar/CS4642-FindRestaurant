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

        def extract_all_css(query):
            return response.css(query).extract()

        def get_facilities(unavailable, all_facilities):
            all_facilities_list= response.css(all_facilities).extract()
            unavailable_list= response.css(unavailable).extract()
            if(all_facilities_list is not None):
                if(unavailable_list is not None):
                    for item in unavailable_list :
                        if(item in all_facilities_list):
                            all_facilities_list.remove(item)
                return all_facilities_list
            elif(unavailable_list is None):
                if(all_facilities_list is not None):
                    return all_facilities_list
            else:
                return all_facilities_list

        yield{
            'name': extract_with_css('#rest-title::text'),
            'address': extract_with_css('div.panel-heading span.address span::text'),
            'servicing_cuisines': extract_all_css('div.panel-body p.cuisine span::text'),
            'open_hours': extract_with_css('#openHours::text'),
            'price_range': extract_with_css('div.panel-body p.price-range span::text'),
            'near_by_restaurants': extract_all_css('#nearbyList li.media a::text')[:-1],
            'rating': extract_with_css('span.rating-total::text'),
            'no_of_reviews': extract_with_css('#review-count::text'),
            'link_to_direction': extract_with_css('a[rel="nofollow"]::attr(href)'),
            'facilities_available': get_facilities('li.info-facility-item.disabled::text','li.info-facility-item::text'),
        }

