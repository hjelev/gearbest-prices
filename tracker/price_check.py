from tracker.parse_url import parse_url
from tracker.send_message import send_message
from tracker.get_old_price import get_old_price
from tracker.config import config

import logging
log = logging.getLogger(__name__)

DB_DIR = config['DEFAULT']['db_dir']
CURRENCY = config['DEFAULT']['currency']
RATE = config['DEFAULT']['rate'] if CURRENCY != 'USD' else 1

def price_check(check_url):
    '''
    Compare prices and availability / emails if there is a change
    '''
    link, price, stock_lvl, product_name = parse_url(check_url)
    old_price,stock_avail = get_old_price(DB_DIR,link,stock_lvl,price) # build the path and open the DB file where last product price is stored

    # NEED TO FIX. UGLY AS HELL!
    price = round(float(price)*float(RATE),2)
    old_price = round(float(old_price.split(",")[0])*float(RATE),2)

    print('')
    print('************** [ITEM] **************')
    print("Name: %s~" % product_name[:60])
    print("URL: %s" % check_url)
    print("New price: ${0}{2} / Old price: ${1}{2}".format(price, old_price, CURRENCY))
    
    change = False
    body = ''

    # checking availability
    if stock_avail == stock_lvl+"\n":  #check for stock level change 
        print("Stock: No changes")
    else:
        change = True
        print("Stock: Availability changed to '%s'!" % stock_lvl)

    # checking price changes
    if price == old_price:
        pass
    else:
        trend = 'raised' if price > old_price else 'dropped'
        change = True
        body += "PRICE | New price: %s The price have %s with %s\nAvailability: %s\n" % (price, trend, float(price) - float(old_price), stock_lvl)

    # sending a message
    if (change and old_price != 0):
        log.debug('***DEBUG. Message will be sent.***')      
        header = "<h2>%s</h2>\n" % product_name
        footer = "<a href='%s'></a>" % check_url
        message = header + body + footer
        # send_message(message, product_name)
            
    return