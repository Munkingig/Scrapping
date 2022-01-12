from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
from pymongo import MongoClient#Manejar Bases De dades MongoDB

#Conectamos con MongoDB.
client = MongoClient('localhost')
db = client['putaaaaaaaaaaaaaaa']
col = db['clima']
col.insert({
    "current":"pooo",
    "real_feel": "awachifil",
    "ciudad":"ciutatipotati",
})

class ExtractorClima(Spider):
    name = "CLIMA"
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
        'LOG_ENABLED': False
    }

    start_urls = [
        "https://www.accuweather.com/es/ec/guayaquil/127947/weather-forecast/127947",
        "https://www.accuweather.com/es/ec/quito/129846/weather-forecast/129846",
        "https://www.accuweather.com/es/es/madrid/308526/weather-forecast/308526"
    ]


    def parse(self, response):
        print("vamos a parsear")
        ciudad = response.xpath('//h1/text()').get()
        current = response.xpath('//div[@class="cur-con-weather-card__panel"]/div[@class="forecast-container"]/div[@class="temp-container"]/div/text()').get()
        real_feel = response.xpath('//div[@class="cur-con-weather-card__panel"]/div[@class="forecast-container"]/div[@class="temp-container"]/div[@class="real-feel"]/text()').get()
        real_feel = real_feel.replace('RealFeel®', '').replace('\n', '').replace('\r', '').strip()
        print("La ciudad es:")
        print(ciudad)
        print("La tempetaruta actual es: ")
        print(current)
        print("La sensacion real es: ")
        print(real_feel)
        print()
    #Se crea el archivo y se guarda todo lo parseado.
        #f = open("./datos_clima_scrapy.csv", "a")
        #f.write(ciudad + "," + current + "," + real_feel + "\n")
        #f.close()

        #Actualizamos o guardamos en un MongoDB.
        col.update_one({
            "ciudad": ciudad
        }, {
            "set": {
                "current": current,
                "real_feel": real_feel,
                "ciudad": ciudad
            }
        }, upsert=True)
        
        col.insert_one({
            'current': current,
            'real_feel': real_feel,
            'ciudad': ciudad
        })


#Para ejecutar el script desde run evitar el comando scrapy runspider.
#process = CrawlerProcess()
#process.crawl(ExtractorClima)
#process.start()

#Para repetir el scrapping periodicamente.
#runner = CrawlerRunner()
#task = LoopingCall(lambda: runner.crawl(ExtractorClima))
#task.start(20)
#reactor.run()