import logging
import os.path
import pickle
import re

from paraback.models.law_model import Law, Link
from paraback.util import get_data_path, suppress_stdout
from tqdm import tqdm


class Linker():

    def link_all(self, law: Law):
        for span in law.get_textspans():
            self.link(span)

    def link(self, span):
        shortlinks = self.extract_shortlinks(span)
        links = [Linker.short_to_long_link(shortlink, span) for shortlink in shortlinks]
        span.links = links

    def extract_shortlinks(self, span):
        return []

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



def main():
    """ Main entry point of the app """

    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)

    datapath = get_data_path()
    sourcepath = os.path.join(datapath, "raw_jsons")
    targetpath = os.path.join(datapath, "linked")

    if not os.path.exists(targetpath):
        os.makedirs(targetpath)

    # iterate over all files in data/raw_jsons
    targets = [f[:-5] for f in os.listdir(os.path.join(datapath, "raw_jsons")) if f.endswith(".json")]
    #targets = ["eWpG"]

    if len(targets) <= 10:
        logger.setLevel(logging.DEBUG)

    for target in (pbar := tqdm(targets)):
        pbar.set_description(target.rjust(30))

        with open(os.path.join(sourcepath, target + ".json")) as fi:
            law = Law.model_validate_json(fi.read())

        linker = RegexLinker()
        linker.link_all(law)

        filename = os.path.join(targetpath, target + ".json")
        if os.path.exists(filename):
            os.remove(filename)
        with open(filename, "w") as fi:
            json = law.model_dump_json(exclude_none=True, indent=2)
            fi.write(json)


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
