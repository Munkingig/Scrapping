import scrapy
from scrapy.item import Field
from scrapy.loader import ItemLoader
from scrapy.item import Item
import time
import random
from scrapy.selector import Selector



class Index(Item):
    numRemota = Field()
    unidadMedida = Field()
    Hora = Field()
    Vb = Field()
    Vc = Field()
    P = Field()
    T = Field()

class StopSpider(scrapy.Spider):
    name = "stop"
    header = {
        'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        'COSESPIDER_PAGECOUNT' : 100,
        'LOG_ENABLED': False,
    }

    start_urls = ["url"]


    def parse(self, response):
    
        yield scrapy.FormRequest('url',
                                formdata={
                                    "_SoyUnPostDeLogin": '1',
                                    "_AuthUsuario": "usuario",
                                    "_AuthPassword":"contraseña",
                                    "_AuthNivel": '1'
                                    },
                                callback=self.parse_Index)


    def parse_Index(self, response):
        sel = Selector(response)
        items = sel.xpath('//form[@id="f"]/table[2]/tr/td/table/tr[3]/td[2]/text()')
        item = ItemLoader(Index(), sel)
        
        item.add_xpath('num', '//form[@id="f"]/h1/a/text()')
        item.add_xpath('unidad', '//form[@id="f"]/table[2]/tr/td/table/tr/th/font/text()')
        
        item.add_xpath('Hora','//form[@id="f"]/table[1]/tr/td/table/tr[3]/td[2]/text()')
        item.add_xpath('Hora','//form[@id="f"]/table[2]/tr/td/table/tr[3]/td[2]/text()')
        item.add_xpath('Vb','//form[@id="f"]/table[2]/tr/td/table/tr[4]/td[2]/text()')
        item.add_xpath('Vc','//form[@id="f"]/table[2]/tr/td/table/tr[5]/td[2]/text()')
        item.add_xpath('P','//form[@id="f"]/table[2]/tr/td/table/tr[6]/td[2]/text()')
        item.add_xpath('T','//form[@id="f"]/table[2]/tr/td/table/tr[7]/td[2]/text()')
        yield item.load_item()

    def startscraper(self, response):
        yield scrapy.Request('url', callback=self.verifylogin)

    def verifylogin(self, response):
        print(response.text)
