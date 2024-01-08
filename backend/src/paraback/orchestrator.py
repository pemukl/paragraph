from paraback.linking.RegexLinker import RegexLinker
from paraback.scraping.downloader import download_target
from paraback.models.law_model import Law, Link
from paraback.scraping.law_builder import LawBuilder
from paraback.saving.InOut import InOut
from paraback.scraping.downloader import landing_to_target


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
        self.html = download_target(landing_to_target(self.url), save=False)

    def parse(self):
        self.law = LawBuilder.build_law(self.html)

    def link(self):
        linker = RegexLinker()
        self.law_linked = linker.link_all(self.law)

    def store(self):
        io = InOut()
        io.write(self.law)

