#!/usr/bin/env python

import web, urllib2, os.path

from bs4 import BeautifulSoup

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

dbdir = "data/" #folder where the DB files will be saved

# configure smtp server for sending mail
web.config.smtp_server = 'smtp.gmail.com'
web.config.smtp_port = 587
web.config.smtp_username = 'username@gmail.com'
web.config.smtp_password = 'password'
web.config.smtp_starttls = True

headers = { 'User-Agent' : 'Mozilla/5.0' } # headers for the url download request

url_list = []
url_list.append("http://www.gearbest.com/batteries-chargers/pp_140785.html")  #usb led light
url_list.append("http://www.gearbest.com/electronics-gadgets/pp_280338.html") # enhanced xiaomi led light

email_list = []
email_list.append("user@gmail.com")
email_list.append("user1@gmail.com")

def send_message(message,product_name): #sends emails to email_list
	for recipient in email_list:
		web.sendmail(web.config.smtp_username, recipient,"Price or Availability Change " + product_name, message, headers={'Content-Type':'text/html;charset=utf-8'})

def get_old_price(dbdir,link,stock_lvl,price): # reads old data and updates it with current data
	db_filename = dbdir + link + ".txt"

	if os.path.isfile(db_filename):  # check if file exists
		log.info('File exist, writing into %s' % db_filename)
		fo = open(db_filename, "r+")
		oldprice = fo.readline() # if there is a file read the previous value
		stock_avail = oldprice.split(",")[1]
		oldprice = oldprice.split(",")[0]
	else:
		fo = open(db_filename, "w+") # create the missing file
		oldprice = "$0" # set previous price to 0
		stock_avail = "Unknown"
		
	position = fo.seek(0, 0)
	fo.write(price+","+stock_lvl+"\n")		# write the new value
	fo.close()

	return oldprice,stock_avail

def parse_url(url): #get current price and availability
	#build the request for the page that will be checked
	req = urllib2.Request(url, None, headers)
	#reads the html 
	html = urllib2.urlopen(req).read()

	link = url.split('/')[4].split('.')[0]

	soup = BeautifulSoup(html, "html.parser") #it'll make this an obj
	
	price = soup.find(attrs={"property":"og:price:amount"}).get('content').encode('utf-8') #get the price
	
	image = soup.findAll(attrs={"property":"og:image"}) #get the image
	image = image[0]['content'].encode('utf-8')
	image = "<img src='" + image + "'>"

	product_name = soup.find(attrs={"property":"og:title"}).get('content').encode('utf-8') #get product name
	
	stock = soup.find_all("a", class_="no_addToCartBtn")
	
	if  len(stock) == 0:
		stock_lvl = "In stock"
	else:
		stock_lvl = "Out of stock"
		
	return link, price, stock_lvl, product_name, image
	
def price_check(check_url):	#compare prices and availability / emails if there is a change
	link, price, stock_lvl, product_name, image = parse_url(check_url)
	oldprice,stock_avail = get_old_price(dbdir,link,stock_lvl,price) # build the path and open the DB file where last product price is stored
	
	print ''
	print '************** [ITEM] **************'
	print "Name: {}~".format(product_name[:60]) 
	print "URL:", check_url
	print "New price: {0} / Old price: {1}".format(price, oldprice.split(",")[0])
	
	price = price.replace("$", "")
	old_price = oldprice.replace("$", "")
	
	change = None
	
	if float(price) > float(old_price):
		message = 'New price: ${} The price have raised with ${}'.format(price, float(price) - float(old_price))
		message = message  + "\nAvailability: "+stock_lvl
		print message + "\n"
		change = True
	elif float(price) < float(old_price): # check if there is a price drop
		message = "New price: ${} The price have droped with ${}".format(price, float(old_price) - float(price))
		message = message  + "\nAvailability: "+stock_lvl
		print message  + "\n"
		change = True
	elif float(price) == float(old_price):
		message = "No change"
		print "No price change \n"

	if stock_avail == stock_lvl+"\n":  #check for stock level change 
		pass
	else:
		change = True
		message = message + "\nAvailability changed to "+stock_lvl+" !"
		print "Availability changed to "+stock_lvl+" !"
		
	message = "<h2>" + product_name + "</h2>" + message + "\n<a href='" + check_url +"'>"+ image +"</a>"

	if (change and old_price != "0"):
		send_message(message,product_name)
			
	return

if __name__ == "__main__":	
	for url in url_list:
		price_check(url)
