import configparser

from tracker.parse_url import parse_url
from tracker.get_old_price import get_old_price

config = configparser.ConfigParser()
config.read('tracker/config.ini')

def price_check(check_url):
    '''
    Compare prices and availability / emails if there is a change
    '''
    link, price, stock_lvl, product_name = parse_url(check_url)
    old_price,stock_avail = get_old_price(config['DEFAULT']['db_dir'],link,stock_lvl,price) # build the path and open the DB file where last product price is stored

    print('')
    print('************** [ITEM] **************')
    print("Name: %s~" % product_name[:60])
    print("URL: %s" % check_url)
    print("New price: $%s / Old price: $%s" % (price, old_price.split(",")[0]))

    change = None

    if float(price) > float(old_price):
        message = 'New price: ${} The price have raised with ${}'.format(price, float(price) - float(old_price))
        message = message  + "\nAvailability: "+stock_lvl
        print(message + "\n")
        change = True
    elif float(price) < float(old_price): # check if there is a price drop
        message = "New price: ${} The price have droped with ${}".format(price, float(old_price) - float(price))
        message = message  + "\nAvailability: "+stock_lvl
        print(message  + "\n")
        change = True
    elif float(price) == float(old_price):
        message = "No change"
        print("No price change \n")

    if stock_avail == stock_lvl+"\n":  #check for stock level change 
        pass
    else:
        change = True
        message = message + "\nAvailability changed to "+stock_lvl+" !"
        print("Availability changed to "+stock_lvl+" !")
        
    message = "<h2>" + product_name + "</h2>" + message + "\n<a href='" + check_url +"'>" + "</a>"

    if (change and old_price != "0"):
        send_message(message,product_name)
            
    return