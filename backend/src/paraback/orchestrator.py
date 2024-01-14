from paraback.linking.regex_linker import RegexLinker
from paraback.scraping.scraper import Scraper
from paraback.scraping.law_builder import LawBuilder
from paraback.saving.mongo_connector import MongoConnector


class Orchestrator():
    def __init__(self, landing_url):
        self.url = landing_url
        self.html = None
        self.law = None
        self.law_linked = None
        self.json = None

    def run(self):
        self.scrape()
        self.parse()
        self.link()
        self.store()

    def scrape(self):
        self.html = Scraper.download_link(self.url)

    def parse(self):
        self.law = LawBuilder.build_law(self.html)

    def link(self):
        linker = RegexLinker()
        self.law_linked = linker.link_all(self.law)

    def store(self):
        io = MongoConnector()
        io.write(self.law)

