import logging
import os.path
import pickle
import re

from paraback.models.law_model import Law, Link
from paraback.util import get_data_path, suppress_stdout, logger
from tqdm import tqdm
from paraback.linking.textspan_linker import TextspanLinker





class RegexTSLinker(TextspanLinker):
    keyword_patterns = None
    confident_pattern = None
    law_name_searcher = None


    def __init__(self, *args, **kwargs):
        if RegexTSLinker.confident_pattern is None:
            keywords_par = r"§§|§|Paragraph|Paragraphen"
            keywords_sec = r"Absatz|Absatzes|Absätze|Absätzen|Abs\."
            keywords_sent = r"Satz|Satzes|Sätze|Sätzen"
            keywords_nr = r"Nummer|Nr\.|Nummern"
            keywords_lit = r"Buchstabe|Buchstaben|Buchst\."
            keyword_pattern = [keywords_par, keywords_sec, keywords_sent, keywords_nr, keywords_lit]

            RegexTSLinker.keyword_patterns = [re.compile(
                RegexTSLinker._build_rough_regex(pat)
            ) for pat in keyword_pattern]

            RegexTSLinker.confident_pattern = re.compile(
                "".join((RegexTSLinker._build_confident_regex(keyword_par)
                          for keyword_par in keyword_pattern
                          ))
            )
        super().__init__(*args, **kwargs)

    @staticmethod
    def _build_confident_regex(tags):
        ordi = r"(?:\d+)[a-z]?"
        joints = r"(?:\s(?:und|bis| ?\- ?)\s)?"

        return \
                r"(?:\s?(?:" + tags + r")\s(" + ordi + r")" \
                + r"(?:(?:,\s(?:" + tags + r"|))\s" + ordi + r")?" \
                + r"(?:" + joints + r"(?:" + tags + r"|)" + ordi + r")?)?"

    @staticmethod
    def _build_rough_regex(tags):
        ordi = r"(?:\d+)[a-z]?"
        return r"(?:\s?(?:" + tags + r")\s(" + ordi + r"))"

    def extract_unrooted_links(self):
        text = self.textspan.text
        self.confident = True

        externals = self.extract_external_links()


        levels = []
        multiple_kws = False
        for i, kw in enumerate(RegexTSLinker.keyword_patterns):
            if found := kw.findall(text):
                if len(found) > 0:
                    levels.append(i)
                if len(found) > 1:
                    multiple_kws = True

        if len(levels) == 0:
            return []

        if len(levels) > 1 and multiple_kws:
            self.confident = False

        matches = self._get_matches()

        if len(matches) == len(externals) and all([match.url.startswith("Par") for match in matches]):
            matches = sorted(matches, key=lambda x: x.start_idx)
            externals = sorted(externals, key=lambda x: x.start_idx)

            for match, external in zip(matches, externals):
                match.url = external.url + "-" + match.url
                match.start_idx = min(match.start_idx, external.start_idx)
                match.stop_idx = max(match.stop_idx, external.stop_idx)
                logger.debug(f"Found ext Link: {text[match.start_idx: match.stop_idx]} ({match.url})")
        elif len(externals)>0:
            matches.extend(externals)
            logger.info("too hard to match externals and internals: " + text)

        return matches


    def _get_matches(self):
        text = self.textspan.text
        links = []

        matches = self.confident_pattern.finditer(text)
        for match in matches:
            res = []
            if match.groups()[:3] == (None, None, None):
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

            logging.debug("Found shortlink " + target + " in '" + self.textspan.text[start:end] + "' of\n-----" + self.textspan.text)
            links.append(Link(start_idx=start, stop_idx=end, url=target, parent_id=self.textspan.id))

        return links




