from http.cookiejar import CookieJar
from bs4 import BeautifulSoup
from urllib import request
import urllib
import time


def create_soup(url_link):
    req = urllib.request.Request(url_link, headers={'User-Agent': 'Mozilla/5.0'})
    cj = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    response = opener.open(req)
    response_source = response.read()
    s = BeautifulSoup(response_source, 'html.parser')
    return s


def all_pages(url_link):
    ss = []
    s = create_soup(url_link)
    size = s.find_all('div', attrs={'class': 'showing'})
    total_pages = int(size[0].contents[0].split()[-2])/int(size[0].contents[0].split()[3])+1
    for i in range(int(total_pages)):
        a = 'https://www.kijiji.ca/b-cars-trucks/city-of-toronto/suv+crossover-2013__2018-used/page-'
        b = '/c174l1700273a138a68a49?price=30000__80000&kilometers=10000__100000'
        page_num = i
        if page_num > 1:
            next_url = ''.join([a, str(page_num), b])
            ss.append(create_soup(next_url))
            print('working on url:', page_num)
            time.sleep(10)
        else:
            ss.append(s)
    return ss


def get_model(soup):
    model = soup.find_all('div', attrs={'class': 'title'})[0:25]
    models = []
    for mod in model:
        if mod.find('a') is None:
            models = models
        elif mod.find('a').contents[0].split()[1] == 'Land':
            models.append(' '.join(mod.find('a').contents[0].split()[3:5]))
        else:
            models.append(''.join(mod.find('a').contents[0].split())[4:9])
    return models


def get_maker(soup):
    maker = soup.find_all('div', attrs={'class': 'title'})[0:25]
    makers = []
    for m in maker:
        if m.find('a') is None:
            makers = makers
        elif len(m.find('a').contents[0].split()) > 2:
            makers.append(m.find('a').contents[0].split()[1])
        elif m.find('a').contents[0].split()[1] == 'Land':
            makers.append(' '.join(m.find('a').contents[0].split()[1:3]))
        else:
            makers.append(''.join(m.find('a').contents[0].split())[9:])
    return makers


def get_year(soup):
    year = soup.find_all('div', attrs={'class': 'title'})[0:25]
    years = []
    for y in year:
        if y.find('a') is None:
            years = years
        elif len(y.find('a').contents[0].split()) > 2:
            years.append(y.find('a').contents[0].split()[0])
        else:
            years.append(int(''.join(y.find('a').contents[0].split())[0:4]))
    return years


def get_price(soup):
    price = soup.find_all('div', attrs={'class': 'price'})[0:25]
    prices = []
    for p in price:
        prices.append(p.contents[0].split()[0][1:].replace(',', ''))
    return prices


def get_km(soup):
    km = soup.find_all('div', attrs={'class': 'details'})[0:25]
    kms = []
    for k in km:
        if len(k.contents[0].split()) < 3:
            kms.append(int(k.contents[0].split()[0][:-2].replace(',', '')))
        else:
            kms.append(int(k.contents[0].split()[2][:-2].replace(',', '')))
    return kms
