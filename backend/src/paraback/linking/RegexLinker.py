import logging
import os.path
import pickle
import re

from paraback.models.law_model import Law, Link
from paraback.util import get_data_path, suppress_stdout
from tqdm import tqdm
from paraback.linking.linker import Linker


def build_regex(tags):
    ord = r"(?:\d+)[a-z]?"
    joints = r"(?:\s(?:und|bis| ?\- ?)\s)?"

    return \
            r"(?:\s?(?:" + tags + r")\s(" + ord + r")" \
            + r"(?:(?:,\s(?:" + tags + r"|))\s" + ord + r")?" \
            + r"(?:" + joints + r"(?:" + tags + r"|)" + ord + r")?)?"


class RegexLinker(Linker):

    def __init__(self):
        regex = build_regex(r"§§|§|Paragraph|Paragraphen")
        regex += build_regex(r"Absatz|Absatzes|Absätze|Absätzen|Abs\.")
        regex += build_regex(r"Satz|Satzes|Sätze|Sätzen")
        regex += build_regex(r"Nummer|Nr\.|Nummern")
        regex += build_regex(r"Buchstabe|Buchstaben|Buchst\.")
        self.pattern = re.compile(regex)

    def extract_shortlinks(self, span):
        text = span.text
        links = []

        matches = self.pattern.finditer(text)
        for match in matches:
            res = []
            if match.groups() == (None, None, None, None, None):
                continue

            if par := match.groups()[0]:
                res.append("Par" + par)

            if sec := match.groups()[1]:
                res.append("Sec" + sec)

            if sent := match.groups()[2]:
                res.append("Sent" + sent)

            if nr := match.groups()[3]:
                res.append("Enum" + nr)

            if lit := match.groups()[4]:
                res.append("Lit" + lit)

            target = "-".join(res)
            start = match.start()
            end = match.end()
            match2 = re.search(r"^\s", text[start:end])
            if match2:
                logging.debug("Found shortlink at start of span: " + text[start:end])
                start += 1

            logging.debug("Found shortlink " + target + " in '" + span.text[start:end] + "' of\n-----" + span.text)
            links.append(Link(start_idx=start, stop_idx=end, url=target, parent_id=span.id))
        return links

