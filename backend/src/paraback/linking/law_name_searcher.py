import re
from typing import Dict

from paraback.models.law_model import TextSpan, Law, Link
from paraback.saving.mongo_connector import MongoConnector
from paraback.llmconnection.name_preprocessor import NamePreprocessor


from ratelimit import limits, RateLimitException, sleep_and_retry



class LawNameSearcher:

    def __init__(self, names: Dict[str, str] = None):
        self.translation_dict = names
        if not self.translation_dict:
            self.get_names_from_mongo()

        if self.translation_dict:
            self.regex = re.compile(r"\b(" + "|".join([f"{re.escape(key)}" for key in self.translation_dict.keys()]) + r")\b")
        else:
            self.regex = re.compile(r"(?!.*)")

        LawNameSearcher.singleton = self

    def get_names_from_mongo(self):
        io = MongoConnector()
        self.translation_dict = io.read_all_names()

    def contained_law_names(self, textspan: TextSpan):
        text = textspan.text
        matches = self.regex.findall(text)
        return [self.translation_dict[match] for match in matches]

    def external_links(self, textspan: TextSpan):
        matches = self.regex.finditer(textspan.text)
        links = []
        for match in matches:
            res = match.group(0)
            target = "DE-"+self.translation_dict[res]
            start = match.start()
            end = match.end()
            link = Link(url=target, start_idx=start, stop_idx=end, parent_id=textspan.id)
            links.append(link)
        return links

    @staticmethod
    @sleep_and_retry
    @limits(calls=4, period=1)
    def find_and_save_name(law: Law):
        name_processor = NamePreprocessor(law)
        variants = name_processor.get_variants()
        variants_dict = {string: law.stemmedabbreviation for string in variants}
        MongoConnector().write_name(variants_dict)
        return law.stemmedabbreviation

# singleton law name searcher
singleton_searcher = LawNameSearcher()