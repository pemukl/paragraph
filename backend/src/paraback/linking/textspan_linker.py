import logging
import os.path
import pickle
import re
from abc import ABC, abstractmethod

from paraback.linking.law_name_searcher import singleton_searcher
from paraback.models.law_model import Law, Link, TextSpan
from paraback.util import get_data_path, suppress_stdout
from tqdm import tqdm


class TextspanLinker(ABC):

    def __init__(self, textspan: TextSpan):
        self.textspan = textspan
        self.confident = False


    def link(self):
        shortlinks = self.extract_unrooted_links()
        links=[]
        for link in shortlinks:
            if TextspanLinker.is_long_link(link):
                links.append(link)
            else:
                links.append(self.root_link(link))
        if len(links) > 0:
            self.textspan.links = links

    def extract_external_links(self):
        matches = []
        if (searcher := singleton_searcher) is not None:
            matches = searcher.external_links(self.textspan)
            if len(matches) > 1:
                self.confident = False
        return matches



    @abstractmethod
    def extract_unrooted_links(self):
        pass

    @staticmethod
    def parse_link_to_dict(string):
        res = {}
        parts = string.split("-")

        for i, part in enumerate(parts):
            if part.startswith("Par"):
                res["par"] = part[3:]
            elif part.startswith("Sec"):
                res["sec"] = part[3:]
            elif part.startswith("Sent"):
                res["sent"] = part[4:]
            elif part.startswith("Enum"):
                res["enum"] = part[4:]
            elif part.startswith("Lit"):
                res["lit"] = part[3:]
            elif part.startswith("SubLit"):
                res["sublit"] = part[6:]
            elif i == 0:
                res["jurisdiction"] = parts[0]
            elif i == 1:
                res["law"] = parts[1]
        return res

    @staticmethod
    def dict_to_link(dic):
        res = []
        if "jurisdiction" in dic:
            res.append(dic["jurisdiction"])
        if "law" in dic:
            res.append(dic["law"])
        if "par" in dic:
            res.append("Par" + dic["par"])
        if "sec" in dic:
            res.append("Sec" + dic["sec"])
        if "sent" in dic:
            res.append("Sent" + dic["sent"])
        if "enum" in dic:
            res.append("Enum" + dic["enum"])
        if "lit" in dic:
            res.append("Lit" + dic["lit"])
        if "sublit" in dic:
            res.append("SubLit" + dic["sublit"])
        return "-".join(res)

    @staticmethod
    def is_long_link(link: Link):
        return link.url.startswith("DE-")

    def root_link(self, unrooted_link):
        context = TextspanLinker.parse_link_to_dict(self.textspan.parent_id)
        shorturl = TextspanLinker.parse_link_to_dict(unrooted_link.url)
        res = {}

        keys = ["jurisdiction", "law", "par", "sec", "sent", "enum", "lit", "sublit"]

        searching = True
        for key in keys:
            if searching and key not in shorturl:
                if key in context:
                    res[key] = context[key]
            else:
                searching = False
                if key in shorturl:
                    res[key] = shorturl[key]

        return Link(start_idx=unrooted_link.start_idx, stop_idx=unrooted_link.stop_idx, url=TextspanLinker.dict_to_link(res),
                    parent_id=unrooted_link.parent_id)

    @classmethod
    def set_law_name_searcher(cls, law_name_searcher):
        cls.law_name_searcher = law_name_searcher
