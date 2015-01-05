# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class Forum81Item(Item):
    first_episode = Field()
    last_episode = Field()
    author = Field()
    title = Field()
    datePosted = Field()


