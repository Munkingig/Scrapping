from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


driver = webdriver.Chrome('./chromedriver.exe')
driver.get('https://www.olx.com.ec')

# Realizar clicl para que se desplegue pla pagina web.
for i in range (3):
    try:
        boton = WebDriverWait(driver, 50).until(
            EC.presence_of_all_elements_located((By.XPATH, '//button[@data-aut-id="btnLoadMore"]'))
        )

        boton.click()
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//li[@data-aut-id="itemBox"]//span[@data-aut-id="itemPrice"]'))
        )
    except:
        break

# Todos los anuncios de una lista.
anuncios = driver.find_elements_by_xpath('//li[@data-aut-id="itemBox"]')

for auto in anuncios:
    precio = auto.find_element_by_xpath('.//span[@data-aut-id="itemPrice"]').text
    print(precio)

    descripcion = auto.find_element_by_xpath('.//span[@data-aut-id="itemTitle"]').text
    print(descripcion)

