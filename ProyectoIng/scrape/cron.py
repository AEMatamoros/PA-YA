from scrape.models import Exchange
import requests
requests.packages.urllib3.disable_warnings()

from bs4 import BeautifulSoup

#JOBS
def scrapcoin():#ScrapeCoinData
    session= requests.Session()
    session.headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; SM-G928X Build/LMY47X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.83 Mobile Safari/537.36'}

    url= 'https://www.bch.hn/'
    content= session.get(url, verify= False).content
    
    soup = BeautifulSoup(content, 'html.parser')

    
    data=   soup.find('div', {'id':'cotizacion'})
    unit = data.find('h3').get_text()
    exchange_data = data.find('span',{'class':'neg'}).get_text()
    
    exchange= Exchange()
    exchange.pk= 1
    exchange.unit = str(unit)
    exchange.unit = "$"
    exchange.exchange = exchange_data
    exchange.save()
    pass


