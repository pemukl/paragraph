import logging
import unittest

from paraback.saving.mongo_connector import MongoConnector
from paraback.scraping.law_builder import LawBuilder
from paraback.scraping.scraper import Scraper
import pytest


class ScraperTest(unittest.TestCase):
    def test_get_links(self):
        logging.log(logging.DEBUG, "scraping all links")
        lists = Scraper._get_all_lists()
        assert(len(lists) > 0)
        landings = Scraper._get_all_landings(lists[0])
        assert(len(landings) > 0)
        for cont in landings:
            assert ("https://www.gesetze-im-internet.de/" in cont)

    def test_landing_to_target(self):
        res = Scraper._landing_to_target("https://www.gesetze-im-internet.de/ewpg/")
        assert("https://www.gesetze-im-internet.de/ewpg/BJNR142310021.html" == res)

    def test_download_link(self):
        res = Scraper.download_link("https://www.gesetze-im-internet.de/ewpg/")
        assert(res is not None)


if __name__ == '__main__':
    unittest.main()
