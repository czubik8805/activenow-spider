from time import sleep

from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess

from spiders.activenow_spider import ActiveNowSpider

load_dotenv()  # take environment variables from .env.

while True:
    c = CrawlerProcess()
    c.crawl(ActiveNowSpider)
    c.start()
    sleep(60)
