NOTICE: THIS SCRIPT IS FOR EDUCATIONAL PURPOSES ONLY. 
ALWAYS READ ROBOT.TXT FILES FOR PERMISSION TO WEBSCRAPE ON ANY WEBSITE

How this webscraper is used:

By pairing this script with a script runner such as Windows Task Scheduler this script can be used to webscrape Craigslist postings which includes: post title, post link, and hours posted. The main dependencies include Selenium and Beautifulsoup4.  

Because these Craigslist postings can go very quickly (esp. free item postings) this webscraper can be used as a way to notify via email address a specific searched item by title. 

This script can also be used for any other category in Craigslists.
After scraping the data main.py uses smtplib to send automated email updates to a particular item.

Conclusion:
This was a cool and creative way to get introduced to web scraping on Python as well as learn how to data websites. 

Dependencies:
Python 3.8.6
astroid           2.5.1
beautifulsoup4    4.9.3
certifi           2020.12.5
chardet           4.0.0
colorama          0.4.4
configparser      5.0.1
crayons           0.4.0
idna              2.10
isort             5.7.0
lazy-object-proxy 1.5.2
mccabe            0.6.1
pip               20.2.1
pylint            2.7.2
requests          2.25.1
selenium          3.141.0
setuptools        49.2.1
soupsieve         2.2
toml              0.10.2
urllib3           1.26.3
webdriver-manager 3.3.0
wrapt             1.12.1
