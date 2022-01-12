import requests
from lxml import html

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

login_form_url = 'https://github.com/login'

session = requests.Session()

login_form_res = session.get(login_form_url, headers=header)

parser = html.fromstring(login_form_res.text)
token_especial = parser.xpath('//input[@name="authenticity_token"]/@value')

login_url = 'https://github.com/session'
login_data = {
    "login": "esto_es_secreto",
    "password":"esto_es_secreto",
    "commit": "Sing in",
    "authenticity_token": "token_especial"
}

session.post(
    login_url,
    data=login_data,
    headers=header,
)

data_url = 'https://github.com/Munkingig?tab=repositories'
respuesta = session.get(
    data_url, headers=header
)

parser = html.fromstring(respuesta.text)
repositorios = parser.xpath('//h3[@class="wb-break-all"]/a/text()')
for repositorio in repositorios:
    print(repositorio)
