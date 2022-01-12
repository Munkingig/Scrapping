from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Articulo(Item):
    titulo = Field()
    contenido = Field()

class Review(Item):
    titulo = Field()
    calificacion = Field()

class Video(Item):
    titulo = Field()
    fecha_de_publicacion = Field()

class IGNCrawler(CrawlSpider):
    name = 'ign'
    custom_settings = {
        'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'COSESPIDER_PAGECOUNT' : 30
    }

    allowed_domains = ['latam.ign.com']

    download_delay = 2  

    start_urls = ['https://latam.ign.com/se/?model=article&q=ps4']

    rules = (
        # Horizontalidad por tipo de informacion
        Rule(
            LinkExtractor(
                allow=r'type='
            ), follow=True, callback="parse_item"
        ),
        # Horizontalidad por paginacion
        Rule(
            LinkExtractor(
                allow=r'&page=\d+'
            ),follow=True
        ),
        # REVIEWS
        Rule(
            LinkExtractor(
                allow=r'/review/'
            ),follow=True, callback='parse_review'
        ),
        # VIDEOS
        Rule(
            LinkExtractor(
                allow=r'/video/'
            ),follow=True, callback='parse_video'
            
        ),
        # ARTICULOS
        Rule(
            LinkExtractor(
                allow=r'/news/'
            ),follow=True, callback='parse_news'
            
        ),
    )

    def parse_news(self, response):
        item = ItemLoader(Articulo(), response)
        item.add_xpath('titulo', '//h1/text()')
        item.add_xpath('contenido', '//div[@id="id_text"]//*/text()')

        yield item.load_item()

    def parse_review(self, response):
        item = ItemLoader(Review(), response)
        item.add_xpath('titulo', '')
        item.add_xpath('calificacion', '//span[@class="side-wrapper side-wrapper hexagon-content"]/text()')

        yield item.load_item()

    def parse_video(self, response):
        item = ItemLoader(Video(), response)
        item.add_xpath('titulo', '')
        item.add_xpath('fecha_de_publicacion', '')

        yield item.load_item()
