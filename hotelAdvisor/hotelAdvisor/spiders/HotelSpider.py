import scrapy
from hotelAdvisor.items import HotelItem
from hotelAdvisor.reviews import ReviewItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
import logging

class HotelSpider(CrawlSpider):
    name = "hotel"
    allowed_domains = ["tripadvisor.in"]
    start_urls = ["https://www.tripadvisor.in/Hotels-g304555-oa0-Jaipur_Jaipur_District_Rajasthan-Hotels.html"]

    rules = (
        Rule(SgmlLinkExtractor(allow=(), restrict_xpaths=('//a[@class="nav next taLnk ui_button primary"]')), callback="parse_hotels", follow= True),
    )

    def parse_hotels(self, response):
        for hotel in response.xpath('//div[@class="prw_rup prw_meta_hsx_three_col_listing"]'):
            item = HotelItem()
            item['_id'] = hotel.xpath('.//a[@class="property_title"]/@id').extract_first().replace('property_', '')
            item['title'] = hotel.xpath('.//a[@class="property_title"]/text()').extract_first()
            rating_div = hotel.xpath('.//div[@class="prw_rup prw_common_rating_and_review_count linespace"]')
            rank = hotel.xpath('.//div[@class="prw_rup prw_common_location_pop_index linespace"]/div//text()').extract_first()
            if '#' in rank:
                rank = rank.split('#')[1].split(' ')[0]
            item['rank'] = rank
            rating = rating_div.xpath('./span/@alt').extract_first()
            if rating:
                item['rating'] = rating.split(' ')[0]
            item['total_reviews'] = rating_div.xpath('./span//text()').extract_first().split(' ')[0]
            yield item;
            yield scrapy.Request(url="https://www.tripadvisor.in"+hotel.xpath('.//a[@class="property_title"]/@href').extract_first(), callback=self.parse_hotelProfile)

    def parse_hotelProfile(self, response):
        href = response.xpath('//div[@class="review-container"]//div[@class="innerBubble"]//a[starts-with(@href, "/ShowUserReviews")]/@href').extract_first()
        if href is not None:
            yield scrapy.Request(url="https://www.tripadvisor.in"+href, callback=self.parse_reviewProfile)

    def parse_reviewProfile(self,response):
        url = response.url
        hotel_id = url[url.find('-d')+2:].split('-')[0]
        for review in response.xpath('//div[@class="innerBubble"]'):
            item = ReviewItem()
            entry_div = review.xpath('.//div[@class="entry"]')
            item['_id'] = entry_div.xpath('.//p//@id').extract_first().replace('review_', '')
            item['review'] = ' '.join(entry_div.xpath('.//p//text()').extract())
            item['hotel_id'] = hotel_id
            rating = review.xpath('.//div[@class="rating reviewItemInline"]/span/@class').extract_first()
            if rating:
                item['rating'] = int(rating.split('_')[3])/10
            time_type_string = review.xpath('.//div[@class="rating-list"]//span//text()').extract_first()
            if "Stayed" in time_type_string:
                travel_time = time_type_string.split(' ')[1]; #specifies month of travel
                item['travel_time'] = travel_time
            if "travelled" in time_type_string:
                travel_type = time_type_string.split(',')[1].split('travelled')[1][1:] #specifies if the person travelled as a couple or with family or any other type
                item['traveller_type'] = travel_type

            yield item
        next_review_url = response.xpath('//a[@class="nav next rndBtn ui_button primary taLnk"]/@href').extract_first()
        if next_review_url is not None:
            yield scrapy.Request(url="https://www.tripadvisor.in"+next_review_url, callback=self.parse_reviewProfile)

