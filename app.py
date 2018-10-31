#!/usr/bin/env python
import sys
from time import sleep

from tracker.price_check import price_check
from tracker.config import config

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

# add your items in the list
url_list = [
	'https://www.gearbest.com/cell-phones/pp_1660531.html',
	'https://www.gearbest.com/robot-vacuum/pp_440546.html',
	'https://www.gearbest.com/electronics-gadgets/pp_310701.html',
	'https://www.gearbest.com/laptops/pp_719203.html',
	'https://www.gearbest.com/brushless-fpv-racer/pp_708379.html',
]

def main():
	period = config['DEFAULT']['period']

	log.info('DB_DIR   : %s' % config['DEFAULT']['db_dir'])
	log.info('CURRENCY : %s' % config['DEFAULT']['currency'])
	log.info('RATE     : %s' % config['DEFAULT']['rate'])
	log.info('PERIOD   : %s seconds' % config['DEFAULT']['period'])

	while True:
		for url in url_list:
			price_check(url)
		log.info('Sleep for %s seconds...' % period)
		sleep(int(period))

if __name__ == "__main__":	
	try:
		main()
	except KeyboardInterrupt:
		log.error('Interrupted by user. Closing the app...')
		sys.exit(0)