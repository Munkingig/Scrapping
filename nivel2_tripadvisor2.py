from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

class Opinion(Item):
    titulo = Field()
    clasificacion = Field()
    contenido = Field()
    autor = Field()



class TripAdvisor(CrawlSpider):
    name = "OpinionesTripAdvisor"
    custom_settings = {
        'USER_AGENT':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'COSESPIDER_PAGECOUNT' : 100
    }

    allowed_domains = ['tripadvisor.es']
    start_urls = ['https://www.tripadvisor.es/Hotels-g303845-Guayaquil_Guayas_Province-Hotels.html']
    download_delay = 1

    rules = (
        # Paginacion de Hoteles (h)
        Rule(
            LinkExtractor(
                allow=r'-oa\d+-'
            ), follow=True
        ),
        # Detalle de hoteles (v)
        Rule(
            LinkExtractor(
                allow=r'/Hotel_Review-',
                restrict_xpaths=['//div[@id="taplc_hsx_hotel_list_lite_dusty_hotels_combined_sponsored_0"]//a[@data-clicksource="HotelName"]']
            ), follow=True
        ),
        # Paginacion de Opiniones dentro de un hotel (h)
        Rule(
            LinkExtractor(
                allow=r'-or\d+-'
            ), follow=True
        ),
        # Detalle de Perfil de usuario (v)
        Rule(
            LinkExtractor(
                allow=r'/Profile/',
                restrict_xpaths=['//div[@data-test-target="reviews-tab"]//a[contains(@class, "ui_header")]']
            ), follow=True, callback='parse_opinion'
        ),
    )

    def parse_opinion(self, response):
        sel = Selector(response)
        opiniones = sel.xpath('//div[@id="content"]/div/div')
        autor = sel.xpath('//h1/span/text()').get()

        for opinion in opiniones:
            item = ItemLoader(Opinion(), opinion)
            item.add_value('autor', autor)
            item.add_xpath('titulo','.//div[@class="social-section-review-ReviewSection__title--dTu08 social section-review-ReviewSection__linked--kl3zg"]/text()')
            item.add_xpath('contenido','.//q/text()')
            item.add_xpath('clasificacion','.//div[contains(@class, "social-section-review")]//span/@class', MapCompose(self.obtenerCalificacion))
            
            yield item.load_item()

    def obtenerCalificacion(self, texto):
        calificacion = texto.split("_")[-1]
        return calificacion