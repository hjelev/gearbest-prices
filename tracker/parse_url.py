import requests
from bs4 import BeautifulSoup

headers = { 'User-Agent' : 'Mozilla/5.0' } # headers for the url download request

def parse_url(url):
    '''
    Get current price and availability
    '''
    r = requests.get(url, headers=headers) 
    soup = BeautifulSoup(r.text, "html.parser") #it'll make this an obj

    link = url.split('/')[4].split('.')[0]
    price = soup.find(attrs={"property":"og:price:amount"}).get('content') #get the price
    product_name = soup.find(attrs={"property":"og:title"}).get('content') #get product name
    stock = soup.find_all("a", class_="no_addToCartBtn")

    if  len(stock) == 0:
        stock_lvl = "In stock"
    else:
        stock_lvl = "Out of stock"
        
    return link, price, stock_lvl, product_name