# gearbest.com products tracker
Price and availability tracker for gearbest.com

---

## Set up
There are two ways of using this script - running on your machine in virtual environment or in Docker container.
Choose which one you'd prefer more and follow the instrtuctions below.

No matter what you've choosen adjust those settings to suit your preferences:

1. Update url_list in app.py:
```
url_list = []
url_list.append("http://www.gearbest.com/batteries-chargers/pp_140785.html")
url_list.append("http://www.gearbest.com/electronics-gadgets/pp_280338.html")
```  
2. Update app's settings in tracker.config.ini
```
currency = NZD
rate = 1.46
```
You can also adjuct other setting to your needs.

## Running in virtual environment

1. Make sure that you're using right version of python in your venv:
```
virtualenv -p python3 .venv
source .venv/bin/activate
pip install -r requirements.txt
```
2. Set up ENVs:   
```
export SMTP_USER = <username@example.com>
export SMTP_PASS = <password>
export SMTP_FROM = <username@example.com>
export SMTP_TO = <your_email_address>
```
3. Run the script:
```
./app.py
```

## Running in Docker

1. Create .env file in app's main directory and populate it with those variables:
```
DOCKER_NAME=<name_for_docker>

SMTP_USER=<username@example.com>
SMTP_PASS=<password>
SMTP_FROM=<username@example.com>
SMTP_TO=<your_email_address>
```
2. Build the image by running
```
make build
```

3. Run the container
```
make local
```
4. Check that everything is working
```
docker ps
docker logs -f <name_for_docker>
```

## Script output example:
```
2018-06-29 09:50:25,816 - tracker.price_check - INFO - ************** [ITEM] **************
2018-06-29 09:50:25,817 - tracker.price_check - INFO - Name: Xiaomi Redmi Note 5 4G Phablet Global Version - $229.99 Free~
2018-06-29 09:50:25,817 - tracker.price_check - INFO - URL: https://www.gearbest.com/cell-phones/pp_1660531.html
2018-06-29 09:50:25,817 - tracker.price_check - INFO - New price: $335.79NZD / Old price: $0.0NZD
2018-06-29 09:50:25,817 - tracker.price_check - INFO - Stock: Availability changed to 'In stock'!
2018-06-29 09:50:25,817 - tracker.price_check - INFO - Sending an email. Please wait a second...
2018-06-29 09:50:30,451 - tracker.price_check - INFO - Email has been sent.
2018-06-29 09:50:30,452 - __main__ - INFO - Sleep for 60 seconds...
```
## Email example:
```
from: ******@gmail.com
to: ******@gmail.com 
Product: Xiaomi Redmi Note 5 4G Phablet Global Version - $229.99 Free
Price: New price - $335.79. The price has raised to $335.79
Availability: In stock
Link: https://www.gearbest.com/cell-phones/pp_1660531.html
```
