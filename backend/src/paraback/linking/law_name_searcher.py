import re
from typing import Dict

from paraback.models.law_model import TextSpan, Law, Link
from paraback.saving.mongo_connector import MongoConnector


class LawNameSearcher:
    singleton = None

    def __init__(self, names: Dict[str, str] = None):
        self.translation_dict = names
        if not self.translation_dict:
            self.get_names_from_mongo()

        self.regex = re.compile(r"\b(" + "|".join([f"{re.escape(key)}" for key in self.translation_dict.keys()]) + r")\b")

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
