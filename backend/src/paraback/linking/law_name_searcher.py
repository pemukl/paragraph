import re
from typing import Dict

from paraback.models.law_model import TextSpan, Law


class LawNameSearcher:
    singleton = None

    def __init__(self, names: Dict[str, str]):
        self.translation_dict = names
        self.regex = re.compile(r"\b(" + "|".join([f"{re.escape(key)}" for key in names.keys()]) + r")\b")

    def contained_law_names(self, textspan: TextSpan):
        text = textspan.text
        matches = self.regex.findall(text)
        print(matches)
        return [self.translation_dict[match] for match in matches]
