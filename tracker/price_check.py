import os

from tracker.parse_url import parse_url
from tracker.send_email import send_email
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
    product_name = product_name[:60]

    log.info('************** [ITEM] **************')
    log.info("Name: %s~" % product_name)
    log.info("URL: %s" % check_url)
    log.info("New price: ${0}{2} / Old price: ${1}{2}".format(price, old_price, CURRENCY))
    
    change = False
    body = ''

    # checking availability
    if stock_avail == stock_lvl+"\n":  #check for stock level change 
        log.info("Stock: No changes")
    else:
        change = True
        log.info("Stock: Availability changed to '%s'!" % stock_lvl)

    # checking price changes
    if price == old_price:
        pass
    else:
        trend = 'raised' if price > old_price else 'dropped'
        change = True
        diff = float(price) - float(old_price)
        body += "Price: New price - $%s. The price has %s to $%s\nAvailability: %s\n" % (price, trend, diff, stock_lvl)

    # sending a message
    # if (change and old_price != 0):
    if (change):

        conf = config['SMTP']
        header = "Product: %s\n" % product_name
        footer = "Link: %s" % check_url
        message = header + body + footer

        log.info('Sending an email. Please wait a second...')

        success = send_email(
            server=conf['server'],
            port=conf['port'],
            subject='GB Prices Notification | Price or stock on one of the items in your list has been changed',
            message=message
        )

        log.info('Email has been sent.') if success else log.error('Something went wrong. Please check the logs.')
            
    return