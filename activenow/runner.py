from dotenv import load_dotenv
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

from spiders.activenow_spider import ActiveNowSpider

load_dotenv(".env")  # take environment variables from .env.


def crawl_job():
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    return runner.crawl(ActiveNowSpider)


def schedule_next_crawl(null, sleep_time):
    """
    Schedule the next crawl
    """
    reactor.callLater(sleep_time, crawl)


def crawl():
    """
    A "recursive" function that schedules a crawl 30 seconds after
    each successful crawl.
    """
    # crawl_job() returns a Deferred
    d = crawl_job()
    # call schedule_next_crawl(<scrapy response>, n) after crawl job is complete
    d.addCallback(schedule_next_crawl, 30)
    d.addErrback(catch_error)


def catch_error(failure):
    print(failure.value)


crawl()
reactor.run()
