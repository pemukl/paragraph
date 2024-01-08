import logging
import os.path
import pickle

import bs4
from bs4 import NavigableString

from paraback.models.law_model import Law, Area, Paragraph, Section, Enumeration, TextSpan, Sentence, Litera, Sublitera
import re
import nltk


from paraback.util import get_data_path, suppress_stdout
from tqdm import tqdm

from contextvars import ContextVar

ctx = ContextVar("context")

class ThreadingLocalContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information from `threading.local` (log_context_data) into the log.
    """
    def __init__(self, attributes):
        super().__init__()
        self.attributes = attributes

    def filter(self, record):
        setattr(record, "context", ctx.get())
        return True

def ordinal(parser):
    def get_ordinal(*args, **kwargs):
        ordinal = parser(*args, **kwargs)
        if ordinal is None:
            return ""
        ordinal = ordinal.replace("-", "–")
        ordinal = ordinal.replace(" ", "")
        ordinal = ordinal.replace(" ", "")
        match = re.match(r"[^\da-zA-Z\(\)\.–•*▪ο□^α-ω]+$", ordinal)
        if match:
            logging.error("Suspicious char '" + match.string + "' in ordinal: " + ordinal)
        return ordinal
    return get_ordinal


class LawBuilder:

    def build_law(html_content):
        soup = bs4.BeautifulSoup(html_content, "html.parser")
        abkspans = soup.find_all("span", {"class": "jnkurzueamtabk"})
        if len(abkspans) != 1:
            tit = soup.head.title.text
            abb = tit.split(" - ")[0]
            title = tit.split(" - ")[1]
            longname = None
        else:
            tit = abkspans[0].text.strip()
            if tit.startswith("("):
                tit = tit[1:]
            if tit.endswith(")"):
                tit = tit[:-1]
            title = tit.split(" - ")[0]
            abb = tit.split(" - ")[1]
            longspans = soup.find_all("span", {"class": "jnlangue"})
            if len(longspans) == 1:
                longname = longspans[0].text
            else:
                longname = None
        stem = abb.replace("-", "–")
        stem = stem.replace(" ", "")
        stem = stem.replace("/", "|")
        stem = stem.replace(" ", "")

        law = Law(longname=longname, title=title, abbreviation=abb, stemmedabbreviation=stem, parent_id="DE")
        ContextVar("context").set(law.id)

        container = soup.find(id="paddingLR12")
        content = []
        last_area = None

        for part in container:
            if isinstance(part, NavigableString):
                continue

            # check if title attribute is set
            if part.has_attr("title"):
                if part.attrs["title"] == "Gliederung":
                    if last_area is not None:
                        content.append(LawBuilder.build_area(last_area, parent=law))
                    last_area = [part]
                elif part.attrs["title"] == "Einzelnorm":
                    if last_area is None:
                        content.append(LawBuilder.build_paragraph(part, parent=law))
                    else:
                        last_area.append(part)
        law.content = content

        return law

    def build_area(parts, parent):
        tit = next(x for x in parts[0].children if not isinstance(x, NavigableString))
        spans = tit.h2.find_all("span", recursive=False)
        if (len(spans) != 2):
            raise Exception("Expected 2 spans in area, got " + str(len(spans)))
        ordinal = spans[0].text
        area = Area(
            title=spans[1].text,
            ordinal=ordinal,
            parent_id=parent.id
        )
        area.content = [LawBuilder.build_paragraph(ezn, area) for ezn in parts[1:]]
        return area

    def build_paragraph(einzelnorm, parent):
        header = einzelnorm.h3
        ord_long = header.find(attrs={"class": "jnenbez"})
        if ord_long:
            ordinal = LawBuilder.get_paragraph_ordinal(ord_long.text)
        else:
            ordinal = None
        title = header.find(attrs={"class": "jnentitel"}).text
        par = Paragraph(ordinal=ordinal, title=title, parent_id=parent.id)
        ctx.set(par.id)
        abss = einzelnorm.find_all(attrs={"class": "jurAbsatz"})
        par.content = [LawBuilder.build_section(abs, par) for abs in abss]
        return par

    @ordinal
    def get_paragraph_ordinal(text):
        match = re.match(r"§ (.*)$", text)
        if match:
            return match.group(1).strip()

        match = re.match(r"§§ (.*)$", text)
        if match:
            logging.info("Need to handle double paragraph: " + text)
            return match.group(1).strip()
        else:
            return text.strip()

    def build_section(absatz, parent):

        text = absatz.text
        ordinal_sec = LawBuilder.get_section_ordinal(text)
        len_ord = 0
        sec = Section(ordinal=ordinal_sec, parent_id=parent.id)
        ctx.set(sec.id)

        if ordinal_sec is not None:
            len_ord = len(ordinal_sec)
        content = LawBuilder.build_enums(absatz, parent=sec, level=0, first_len=len_ord)

        pointgroups = [[]]
        for point in content:
            txt = point.to_text().strip()
            if len(txt) == 0:
                continue
            parts = LawBuilder.split_into_sentences(txt)
            if (len(parts) <= 1):
                if len(parts) == 0:
                    logging.debug("empty parts of text: " + txt)
                if (txt.endswith(".")):
                    pointgroups[-1].append(point)
                    pointgroups.append([])
                else:
                    pointgroups[-1].append(point)
            else:
                if isinstance(point, TextSpan):
                    for part in parts[:-1]:
                        if len(part) == 0:
                            continue
                        pointgroups[-1].append(TextSpan(text=part, parent_id=sec.id))
                        pointgroups.append([])
                    pointgroups[-1].append(TextSpan(text=parts[-1], parent_id=sec.id))
                    if parts[-1].strip().endswith("."):
                        pointgroups.append([])
                else:
                    logging.debug(str(point.type) + " contains multiple dots:\n " + txt)

        sents = [Sentence(content=pts, ordinal=str(i + 1), parent_id=sec.id) for i, pts in enumerate(pointgroups) if
                 len(pts) > 0]
        if (len(sents) > 1):
            content = sents
            for sent in content:
                for cont in sent.content:
                    cont.parent_id = sent.id

        sec.content = content
        return sec

    @ordinal
    def get_section_ordinal(text):
        match = re.match(r"^\((\S+)\)", text)
        len_ord = 0

        if match:
            ordinal_sec = match.group(1)
            len_ord = len(ordinal_sec)
            return ordinal_sec

    def build_enums(enum, parent, level=0, first_len=0):
        content = []

        for point in enum.children:

            if isinstance(point, NavigableString) or point.name == "notindexed" or point.name == "span":
                text = point.text
                if first_len > 0:
                    text = text[first_len + 2:]
                    first_len = 0
                if len(text) > 0:
                    content.append(TextSpan(text=text, parent_id=parent.id))
                continue
            else:
                if first_len > 0:
                    logging.info("Could not strip paragraph ordinal because of non-known type: " + str(point))


            if point.name == "dl":
                ordinal = None
                for subpoint in point.children:
                    if subpoint.name == "dt":
                        ordinal = LawBuilder.get_enum_ordinal(subpoint.text, level)
                    elif subpoint.name == "dd":
                        if ordinal is None:
                            logging.warning("Careful: Ordinal is not set: " + subpoint.text)
                        pt = None
                        if level == 0:
                            pt = Enumeration(ordinal=ordinal, parent_id=parent.id)
                        elif level == 1:
                            pt = Litera(ordinal=ordinal, parent_id=parent.id)
                        elif level == 2:
                            pt = Sublitera(ordinal=ordinal, parent_id=parent.id)

                        if pt is not None:
                            pt.content = LawBuilder.build_enums(subpoint, parent=pt, level=level + 1)
                            content.append(pt)
                        else:
                            logging.info("level " + str(level) + " not implemented")


                    elif subpoint.text == "\n":
                        continue
                    else:
                        logging.warning("unused " + str(subpoint) + ": " + subpoint.text)

            elif point.name == "div":
                content += LawBuilder.build_enums(point, parent=parent, level=level)
            elif point.name == "br":
                continue
            elif point.name in ["table","img", "a"]:
                logging.info("Cannot (yet) content of type: " + str(point.name) + ": " + point.text)
            elif point.name in ["sup", "sub", "pre", "cite"]:
                logging.info("Cannot (yet) do formatting of type: " + str(point.name) + ": " + point.text)
            else:
                logging.warning("unused " + str(point) + ": " + point.text)


        return content

    def split_into_sentences(txt):
        tokenizer = nltk.data.load('tokenizers/punkt/german.pickle')
        res = tokenizer.tokenize(txt)
        out = []
        carry = ""
        for sent in res:
            carry += sent
            if carry.count("(") <= carry.count(")"):
                out.append(carry)
                carry = ""

        return out

    @ordinal
    def get_enum_ordinal(text, level):
        if level == 0:
            match = re.match(r"(\S+)\.", text)
            if match:
                ordinal = match.group(1)
                return ordinal

        elif level == 1:
            match = re.match(r"([a-z])\)", text)
            if match:
                ordinal = str(match.group(0))
                return ordinal

        elif level == 2:
            match = re.match(r"([a-z])\1", text)
            if match:
                ordinal = str(match.group(0))
                return ordinal

        return text


def main():
    """ Main entry point of the app """

    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter('{context} {levelname}: {message}', style='{'))
    handler.addFilter(ThreadingLocalContextFilter(['context']))
    logger.addHandler(handler)

    path = get_data_path()

    errs = 0
    succs = 0
    targets = os.listdir(os.path.join(path, "htmls"))
    #targets = ["mkseuchv_2005.html"]

    if len(targets) <= 3:
        logger.setLevel(logging.DEBUG)

    for html_name in (pbar := tqdm(targets)):
        ctx.set(html_name)
        pbar.set_description(html_name.rjust(30))
        if not html_name.endswith(".html"):
            continue
        with open(os.path.join(path, "htmls", html_name)) as f:
            html_content = f.read()
            try:
                law = LawBuilder.build_law(html_content)
                law.model_rebuild()
                succs += 1
            except Exception as e:
                errs += 1
                logging.error("Error while parsing " + html_name + ": " + str(e))
                raise e
                continue
        target_folder = os.path.join(path, "raw_jsons")
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        filename = os.path.join(target_folder, law.stemmedabbreviation+".json")
        if os.path.exists(filename):
            os.remove(filename)
        with open(filename, "w") as fi:
            json = law.model_dump_json(exclude_none=True, indent=2)
            fi.write(json)

    #print("Parsed HTMLs with " + str(errs) + " errors and " + str(succs) + " successes. Thats " + str(
    #    round(succs / (errs + succs) * 100, 2)) + "% success rate.")


if __name__ == "__main__":
    main()
