import logging
import os.path
import pickle
import re
from abc import ABC, abstractmethod

from paraback.models.law_model import Law, Link, TextSpan
from paraback.util import get_data_path, suppress_stdout
from tqdm import tqdm


class Linker(ABC):

    def link_all(self, law: Law):
        for span in law.get_textspans():
            self.link(span)

    def link(self, span: TextSpan):
        shortlinks = self.extract_shortlinks(span)
        links = [Linker.short_to_long_link(shortlink, span) for shortlink in shortlinks]
        span.links = links

    @abstractmethod
    def extract_shortlinks(self, span):
        pass


    @staticmethod
    def parse_link(string):
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
    def short_to_long_link(shortlink, span):
        context = Linker.parse_link(span.parent_id)
        shorturl = Linker.parse_link(shortlink.url)
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

        return Link(start_idx=shortlink.start_idx, stop_idx=shortlink.stop_idx, url=Linker.dict_to_link(res),
                    parent_id=shortlink.parent_id)


