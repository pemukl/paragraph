from paraback.linking.law_name_searcher import LawNameSearcher
from paraback.linking.regex_ts_linker import RegexTSLinker
from paraback.linking.openai_ts_linker import OpenAITSLinker


class LawNameSearcherMissingException(Exception):
    pass

class LawLinker:
    law_name_searcher = None
    def __init__(self, law):
        self.law = law

    def set_law_name_searcher(self, law_name_searcher):
        LawLinker.law_name_searcher = law_name_searcher

    def link(self):
        if not LawLinker.law_name_searcher:
            self.law_name_searcher = LawNameSearcher()

        unclear = []
        for span in self.law.get_textspans():
            linker = RegexTSLinker(span)
            linker.set_law_name_searcher(LawLinker.law_name_searcher)
            linker.link()
            if not linker.confident:
                unclear.append(span)

        for span in unclear:
            linker = OpenAITSLinker(span)
            linker.link()

