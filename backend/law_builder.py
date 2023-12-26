import logging

import bs4
from bs4 import NavigableString

from law_model import Law, Area, Paragraph, Section, Enumeration, TextSpan, Sentence, Litera, Sublitera
import re
import os
import nltk



class LawBuilder():
    def build_law(html_content):
        soup = bs4.BeautifulSoup(html_content, "html.parser")
        title = soup.head.title.text
        law = Law(title=title.split(" - ")[1], abbreviation=title.split(" - ")[0], parent_id="DE")

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
        spans = tit.h2.find_all("span",recursive=False)
        if(len(spans) != 2):
            raise Exception("Expected 2 spans in area, got "+str(len(spans)))
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
        ordinal = LawBuilder.get_paragraph_ordinal(ord_long.text)
        title = header.find(attrs={"class": "jnentitel"}).text
        abss = einzelnorm.find_all(attrs={"class": "jurAbsatz"})
        par = Paragraph(ordinal=ordinal,title=title, parent_id=parent.id)
        par.content = [LawBuilder.build_section(abs,par) for abs in abss]
        return par

    def get_paragraph_ordinal(text):
        match = re.match(r"§ (.*)$", text)
        if match:
            return match.group(1).strip()

        match = re.match(r"§§ (.*)$", text)
        if match:
            logging.warning("Need to handle double paragraph: " + text)
            return match.group(1).strip()

        else:
            logging.warning("Paragraph ordinal might be wrong: "+text)
            return text.strip()

    def build_section(absatz, parent):
        ordinal_sec = None

        text = absatz.text
        ordinal_sec = LawBuilder.get_section_ordinal(text)
        len_ord = 0
        sec = Section(ordinal=ordinal_sec, parent_id=parent.id)

        if ordinal_sec is not None:
            len_ord = len(ordinal_sec)
        content = LawBuilder.build_enums(absatz, parent=sec, level=0, first_len = len_ord)

        pointgroups = [[]]
        for point in content:
            txt = point.to_text().strip()
            if len(txt) ==0:
                continue
            parts = LawBuilder.split_into_sentences(txt)
            if(len(parts) == 1):
                if(txt.endswith(".")):
                    pointgroups[-1].append(point)
                    pointgroups.append([])
                else:
                    pointgroups[-1].append(point)
            else:
                if isinstance(point, TextSpan):
                    if len(parts) ==0:
                        logging.warning("empty parts of text: "+txt)
                    for part in parts[:-1]:
                        if len(part) == 0:
                            continue
                        pointgroups[-1].append(TextSpan(text=part, parent_id=sec.id))
                        pointgroups.append([])
                    pointgroups[-1].append(TextSpan(text=parts[-1], parent_id=sec.id))
                    if parts[-1].strip().endswith("."):
                        pointgroups.append([])
                else:
                    logging.warning(str(type(point))+" contains multiple dots:\n "+txt)

        sents = [Sentence(content=pts,ordinal=i+1,parent_id=sec.id) for i,pts in enumerate(pointgroups) if len(pts) > 0]
        if(len(sents) > 1):
            content = sents
            for sent in content:
                for cont in sent.content:
                    cont.parent_id = sent.id

        sec.content = content
        return sec

    def get_section_ordinal(text):
        match = re.match(r"^\((\S+)\)", text)
        len_ord = 0

        if match:
            ordinal_sec = match.group(1)
            len_ord = len(ordinal_sec)
            return ordinal_sec



    def build_enums(enum, parent, level = 0, first_len = 0):
        content = []
        ordinal = None
        for point in enum.children:
            text = point.text
            if first_len > 0:
                text = text[first_len + 2:]
                first_len =0
                if not isinstance(point, NavigableString):
                    logging.warning("first_len > 0 but point is not NavigableString: "+str(point))

            if isinstance(point, NavigableString):
                if len(text) > 0:
                    content.append(TextSpan(text=text, parent_id=parent.id))
            elif point.name == "dl":
                ordinal = None
                for subpoint in point.children:
                    if subpoint.name == "dt":
                        ordinal = LawBuilder.get_enum_ordinal(subpoint.text, level)
                    elif subpoint.name == "dd":
                        if ordinal is None:
                            logging.warning("Careful: Ordinal is not set: "+subpoint.text)
                        pt = None
                        if level == 0:
                            pt = Enumeration(ordinal=ordinal, parent_id=parent.id)
                        elif level == 1:
                            pt = Litera(ordinal=ordinal, parent_id=parent.id)
                        elif level == 2:
                            pt = Sublitera(ordinal=ordinal, parent_id=parent.id)

                        pt.content = LawBuilder.build_enums(subpoint, parent = pt, level=level+1)
                        content.append(pt)

                    elif subpoint.text == "\n":
                        continue
                    else:
                        logging.warning("unused " + str(subpoint) + ": " + subpoint.text)

            elif point.name == "div":
                content += LawBuilder.build_enums(point, parent=parent, level=level)

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

    def get_enum_ordinal(text, level):
        if level == 0:
            match = re.match(r"(\S+)\.", text)
            if match:
                ordinal = match.group(1)
                return ordinal

        elif level == 1:
            match = re.match(r"([a-z])\)", text)
            if match:
                ordinal = ord(match.group(1))-ord("a")+1
                return ordinal

        elif level == 2:
            match = re.match(r"([a-z])\1", text)
            if match:
                ordinal = ord(match.group(1)) - ord("a") + 1
                return ordinal

        logging.warning("no proper ordinal found in " + text)
        return text
def main():
    """ Main entry point of the app """
    nltk.download('punkt')

    targets = [
        "ewpg",
        "kredwg",
        "aktg",
        "kagb"
    ]

    for target in targets:
        with open("htmls/"+target+".html") as f:
            html_content = f.read()
            law = LawBuilder.build_law(html_content)

        with open("jsons/"+law.abbreviation+".json", "w") as fi:
            fi.write(law.json())

        with open("../frontlex/src/lib/autolaw/"+law.abbreviation+".json", "w") as fi:
            fi.write(law.json())

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()