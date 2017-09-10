from scrapy.item import Item, Field

class ReviewItem(Item):
    _id = Field()
    review = Field()
    hotel_id = Field()
    rating = Field()
    traveller_type = Field()
    travel_time = Field()

