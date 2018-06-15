# gearbest.com products tracker
Price and availability tracker for gearbest.com

---

## Before running the script for a first time, configure it by updating  these lines:
````
url_list = []
url_list.append("http://www.gearbest.com/batteries-chargers/pp_140785.html")  #usb led light
url_list.append("http://www.gearbest.com/electronics-gadgets/pp_280338.html") # enhanced xiaomi led light

email_list = []
email_list.append("user@gmail.com")
email_list.append("user1@gmail.com")
````
and make sure you have these python modules installed: 
- beautifulsoup4
- requests
- configparser
- logging
```
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run this script with a cron job and you'll get an email each time there are price or availability changes in the list of tracked urls.

## Cronjob example:
````
10 */1 * * * /usr/bin/python /home/user/gearbest/gearbetst-prices.py
````
In this example the script will run once per hour and notify you if there is a change.

## Script output example:
````
Availability changed to Out of stock !
Original Xiaomi Portable USB LED Light ( Enhanced Edition )
url: http://www.gearbest.com/electronics-gadgets/pp_280338.html
New price: $3.64  / Old price:  $3.64 No price change

5mm Square Magnetic Block - 216Pcs
url: http://www.gearbest.com/other-classic-toys/pp_271768.html
New price: $20.82  / Old price:  $20.82 No price change

Original Xiaomi Yeelight E27 Smart LED Bulb
url: http://www.gearbest.com/smart-light-bulb/pp_278478.html?wid=21
New price: $12.99  / Old price:  $12.99 No price change

````

Python 2.7
		
This script uses BeautifulSoup, Webpy and needs a folder to store previous product data.
