import re

from law_model import Law, Link


class Linker():

    def __init__(self, law: Law):
        self.law = law

    def link_all(self):
        for span in self.law.get_textspans():
            self.__class__.link(span)

    @classmethod
    def link(cls, span):
        shortlinks = cls.extract_shortlinks(span)
        links = [Linker.short_to_long_link(shortlink, span) for shortlink in shortlinks]
        span.links = links

    @classmethod
    def extract_shortlinks(cls,span):
        return []

    @staticmethod
    def parse_link(string):
        res = {}
        parts = string.split("-")

        for i,part in enumerate(parts):
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
            res.append("Par"+dic["par"])
        if "sec" in dic:
            res.append("Sec"+dic["sec"])
        if "sent" in dic:
            res.append("Sent"+dic["sent"])
        if "enum" in dic:
            res.append("Enum"+dic["enum"])
        if "lit" in dic:
            res.append("Lit"+dic["lit"])
        if "sublit" in dic:
            res.append("SubLit"+dic["sublit"])
        return "-".join(res)

    @staticmethod
    def short_to_long_link(shortlink, span):
        context = Linker.parse_link(span.parent_id)
        shorturl = Linker.parse_link(shortlink.url)
        res = {}

        keys = ["jurisdiction","law","par","sec","sent","enum","lit","sublit"]

        searching = True
        for key in keys:
            if searching and key not in shorturl:
                if key in context:
                    res[key] = context[key]
            else:
                searching = False
                if key in shorturl:
                    res[key] = shorturl[key]

        return Link(start_idx=shortlink.start_idx, stop_idx=shortlink.stop_idx, url=Linker.dict_to_link(res), parent_id=shortlink.parent_id)

class RegexLinker(Linker):
    @classmethod
    def extract_shortlinks(cls, span):
        links = []
        matches = re.finditer(r"(?:§ (\d+))?(?: ?(?:Absatz|Abs\.) (\d+))?(?: ?Satz (\d+))?(?: ?(?:Nummer|Nr\.) (\d+))?", span.text)
        for match in matches:
            res = []
            if match.groups() == (None, None, None, None):
                continue
            par = match.groups()[0]
            if par:
                res.append("Par"+par)

            abs = match.groups()[1]
            if abs:
                res.append("Sec"+abs)

            sent = match.groups()[2]
            if sent:
                res.append("Sent"+sent)

            nr = match.groups()[3]
            if nr:
                res.append("Enum"+nr)
            target = "-".join(res)
            links.append(Link(start_idx=match.start(), stop_idx=match.end(), url=target, parent_id=span.id))
        return links


def main():
    """ Main entry point of the app """

    targets = [
        "eWpG",
    #    "KWG",
    #    "AktG",
    #    "KAGB"
    ]

    for target in targets:
        with open("jsons/" + target + ".json") as fi:
            law = Law.parse_raw(fi.read())

        linker = RegexLinker(law)
        linker.link_all()

        with open("linked/"+law.abbreviation+".json", "w") as fi:
            fi.write(law.json())

        with open("../frontlex/src/lib/autolaw/"+law.abbreviation+".json", "w") as fi:
            fi.write(law.json())



if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()