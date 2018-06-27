#!/usr/bin/env python
from tracker.price_check import price_check

url_list = []

# add here ITEMs that you'd like to monitor
url_list.append("http://www.gearbest.com/batteries-chargers/pp_140785.html")  #usb led light
url_list.append("http://www.gearbest.com/electronics-gadgets/pp_280338.html") # enhanced xiaomi led light
url_list.append('https://www.gearbest.com/cell-phones/pp_1660531.html')

if __name__ == "__main__":	
	for url in url_list:
		price_check(url)
