from paraback.linking.law_name_searcher import LawNameSearcher
from paraback.linking.openai_textspan_linker import OpenAITSLinker
from paraback.linking.regex_textspan_linker import RegexTSLinker
from paraback.linking.textspan_linker import TextspanLinker


class HybridTSLinker(TextspanLinker):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def extract_unrooted_links(self):
        working_copy = self.textspan.model_copy(deep=True)


        linker = RegexTSLinker(working_copy)
        shortlinks = linker.extract_unrooted_links()
        if linker.confident:
            return shortlinks

        ai_linker = OpenAITSLinker(self.textspan)
        ai_links = ai_linker.extract_unrooted_links()
        if len(ai_links) > 0:
            return ai_links
        return shortlinks