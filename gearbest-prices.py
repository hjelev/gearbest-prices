#!/usr/bin/env python

import os.path, configparser
from tracker.price_check import price_check

url_list = []
url_list.append("http://www.gearbest.com/batteries-chargers/pp_140785.html")  #usb led light
url_list.append("http://www.gearbest.com/electronics-gadgets/pp_280338.html") # enhanced xiaomi led light

email_list = []
email_list.append("user@gmail.com")
email_list.append("user1@gmail.com")

# def send_message(message,product_name): #sends emails to email_list
# 	for recipient in email_list:
# 		smtp_config = config['WEB']
# 		web.sendmail(smtp_config.smtp_username,
# 					smtp_config.recipient,
# 					"Price or Availability Change " + product_name,
# 					message,
# 					headers={'Content-Type':'text/html;charset=utf-8'})

if __name__ == "__main__":	
	for url in url_list:
		price_check(url)
