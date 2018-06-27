import configparser

from tracker.parse_url import parse_url
from tracker.send_message import send_message
from tracker.get_old_price import get_old_price

config = configparser.ConfigParser()
config.read('tracker/config.ini')

DB_DIR = config['DEFAULT']['db_dir']
RATE = config['DEFAULT']['rate'] if config['DEFAULT']['currency'] != 'USD' else 1

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
    print("New price: $%s / Old price: $%s" % (price, old_price))
    
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
        print('***DEBUG. Message will be sent.***')      
        header = "<h2>%s</h2>\n" % product_name
        footer = "<a href='%s'></a>" % check_url
        message = header + body + footer
        # send_message(message, product_name)
            
    return