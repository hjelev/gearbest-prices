#!/usr/bin/env python
from time import sleep

from tracker.price_check import price_check
from tracker.config import config

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

url_list = []

# add here ITEMs that you'd like to monitor
# url_list.append("http://www.gearbest.com/batteries-chargers/pp_140785.html")  #usb led light
# url_list.append("http://www.gearbest.com/electronics-gadgets/pp_280338.html") # enhanced xiaomi led light
url_list.append('https://www.gearbest.com/cell-phones/pp_1660531.html')

def main():

	periodicity = config['DEFAULT']['periodicity']

	log.info('DB_DIR    : %s' % config['DEFAULT']['db_dir'])
	log.info('CURRENCY  : %s' % config['DEFAULT']['currency'])
	log.info('RATE      : %s' % config['DEFAULT']['rate'])

	while True:

		for url in url_list:
			price_check(url)
		
		log.info('Sleep for %s seconds...' % periodicity)
		sleep(int(periodicity))

if __name__ == "__main__":	
	main()