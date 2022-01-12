import schedule#Modulo para repeticiones
import time
from selenium import webdriver #Modulo para manejar el driver de selenium
from pymongo import MongoClient#Manejar Bases De dades MongoDB

#Conectamos con MongoDB.
client = MongoClient('localhost')
db = client('weather')
col = db['clima']


start_urls = [
        "https://www.accuweather.com/es/ec/guayaquil/127947/weather-forecast/127947",
        #"https://www.accuweather.com/es/ec/quito/129846/weather-forecast/129846",
        #"https://www.accuweather.com/es/es/madrid/308526/weather-forecast/308526"
]

def extraer_datos():
    driver = webdriver.Chrome('./chromedriver.exe')

    # Por cada una de las URLs que quiero extraer...
    for url in start_urls:

        # Voy en mi navegador a cada URL
        driver.get(url)

        # Extraigo los datos
        ciudad = driver.find_element_by_xpath('//h1').text
        #current = driver.find_element_by_xpath('//div[contains(@class, "cur-con-weather-card__panel")]/div[contains(@class, "forecast-container")]/div[contains(@class, "temp-container")]/div[contains(@class, "temp")]').text
        #real_feel = driver.find_element_by_xpath('//div[@class="cur-con-weather-card__panel"]//div[@class="forecast-container"]//div[@class="temp-container"]//div[@class="real-feel"]').text
        #real_feel = real_feel.replace('RealFeel®', '').replace('\n', '').replace('\r', '').strip()

        print("La ciudad es:")
        print(ciudad)
        print("La tempetaruta actual es: ")
        print(current)
        print("La sensacion real es: ")
        #print(real_feel)
        print()

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

        #Se crea el archivo
        #f = open("./datos_clima_selenium.csv", "a")
        #f.write(ciudad + "," + current + "," + real_feel + "\n")
        #f.close()
    # Cierro el navegador
    driver.close()

extraer_datos()
# Logica de schedule (ver documentacion en recursos)
schedule.every(1).minutes.do(extraer_datos) # Cada 1 minuto ejecutar la funcion extraer_datos

# Reviso la cola de procesos cada segundo, para verificar si tengo que correr algun proceso pendiente
while True:
    schedule.run_pending() # Correr procesos que esten pendientes de ser ejecutados.
    time.sleep(1) # Para no saturar el CPU de mi maquina (por el while true), espero 1 segundo entre cada iteracion

