import os, smtplib
from email.mime.text import MIMEText as text

import logging
log = logging.getLogger(__name__)

def send_email(server, port, subject, message):

    # Get ENV variables to send an email
    SMTP_USER = os.getenv('SMTP_USER')
    SMTP_PASS = os.getenv('SMTP_PASS')
    SMTP_FROM = os.getenv('SMTP_FROM')
    SMTP_TO = os.getenv('SMTP_TO')

    # check if ENV exist
    if not SMTP_USER or not SMTP_PASS or not SMTP_FROM or not SMTP_TO:
        log.error('No credetials provided.')
        return 0

    # create structure of email
    email = text(message)
    email['Subject'] = subject
    email['From'] = SMTP_FROM
    email['To'] = SMTP_TO

    # sending an email
    try:
        smtp = smtplib.SMTP('%s:%s' % (server, port))
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASS)
        smtp.sendmail(SMTP_FROM, SMTP_TO, email.as_string())
        smtp.quit()
        return 1
        
    except smtplib.SMTPException as e:
        log.error(e)
        return 0