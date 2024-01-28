from paraback.linking.hybrid_textspan_linker import HybridTSLinker
from paraback.linking.law_name_searcher import LawNameSearcher
from paraback.saving.mongo_connector import MongoConnector


class LawNameSearcherMissingException(Exception):
    pass

class LawLinker:
    law_name_searcher = None
    def __init__(self, law):
        self.law = law


    def link(self):
        if not LawLinker.law_name_searcher:
            self.law_name_searcher = LawNameSearcher()

        unclear = []
        for span in self.law.get_textspans():
            linker = HybridTSLinker(span)
            linker.link()

    @staticmethod
    def link_and_save_law(law):
        linker = LawLinker(law)
        linker.set_law_name_searcher(LawNameSearcher())
        linker.link()
        io = MongoConnector(db="laws", collection="de")
        io.write(law)
