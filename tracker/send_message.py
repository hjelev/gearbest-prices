import logging
log = logging.getLogger(__name__)

email_list = []
email_list.append("user@gmail.com")
email_list.append("user1@gmail.com")

def send_message(message,product_name):
	"""sends emails to email_list"""
	for recipient in email_list:
		logging.info('Sending a message to %s about %s' % recipient, product_name)
		smtp_config = config['WEB']
		web.sendmail(smtp_config.smtp_username,
					smtp_config.recipient,
					"Price or Availability Change " + product_name,
					message,
					headers={'Content-Type':'text/html;charset=utf-8'})