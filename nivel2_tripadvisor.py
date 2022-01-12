from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Hotel(Item):
    nombre = Field()
    precio = Field()
    descripcion = Field()
    aumenties = Field()

class TripAdvisor(CrawlSpider):
    name = "Hoteles"
    custom_settings = {
        'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'LOG_ENABLED': False,
    }
    start_urls = ['https://www.tripadvisor.es/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']
#Tiempo de espera para navegar a la siguiente pagina.(Simular que navega un persona).
    download_delay = 2
#Reglas para la navegacion etre paginas
    rules = (
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-'
            ), follow=True, callback="parse_item"
        ),
    )

    def quitarSimboloDolar(self, texto):
        nuevoTexto = texto.replace("$", "")
        nuevoTexto = nuevoTexto.replace('\n', '').replace('\r', '').replace('\t', '').replace("€", '')
        return nuevoTexto

    def parse_item(self, response):
        sel = Selector(response)#Parseador del arbol
        item = ItemLoader(Hotel(), sel)

        item.add_xpath('nombre', '//h1[@id="HEADING"]/text()')
        item.add_xpath('precio', '//div[@class="ui_columns is-mobile is-multiline is-vcentered is-gapless-vertical _2mWM5u8t"]/div[2]/div/text()', MapCompose(self.quitarSimboloDolar))
        item.add_xpath('precio', '//div[@class="ui_columns is-gapless is-mobile"]/div[2]/div/div/text()', MapCompose(self.quitarSimboloDolar))
        item.add_xpath('descripcion', '//div[contains(@class, "hotel-review-about-csr-Description__description")]/div[1]/text()')
        item.add_xpath('amenities', '//div[contains(@class, "hotels-hr-about-amenities-Amenity__amenity")]/text()')

        yield item.load_item()
