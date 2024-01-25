from __future__ import annotations
import json
import logging
from abc import ABC, abstractmethod
from pydantic import Field, ConfigDict

from typing import List, Optional, Dict, Any, Literal, Union, Annotated

from pydantic import BaseModel

class JurModel(BaseModel):
    parent_id: str

    model_config = ConfigDict(extra='ignore')

    @property
    def tag(self: JurModel):
        if isinstance(self, Paragraph):
            return "Par"
        if isinstance(self, Section):
            return "Sec"
        if isinstance(self, Sentence):
            return "Sent"
        if isinstance(self, Enumeration):
            return "Enum"
        if isinstance(self, Litera):
            return "Lit"
        if isinstance(self, Sublitera):
            return "SubLit"

    @property
    def id(self):
        if self.tag is not None:
            if self.ordinal is not None:
                return self.parent_id + "-" + self.tag + str(self.ordinal)
            elif hasattr(self, "title") and self.title is not None:
                return self.parent_id + "-" + self.tag + self.title
            else:
                return self.parent_id
        else:
            return self.parent_id

    def dict(self, *args, **kwargs) -> Dict[str, Any]:
        kwargs.pop('exclude_none', None)
        return super().dict(*args, exclude_none=True, **kwargs)

    def to_text(self):
        if hasattr(self, "text"):
            return self.text
        if hasattr(self, "content"):
            if isinstance(self.content, list):
                return "".join([x.to_text() for x in self.content])
            elif isinstance(self.content, str):
                return self.content
        else:
            logging.warning("no text found in " + str(self))

    def get_textspans(self):
        """get all textspans from content"""
        if (isinstance(self, TextSpan)):
            yield self
        if (hasattr(self, "content") and isinstance(self.content, list)):
            for x in self.content:
                yield from x.get_textspans()


class Link(JurModel):
    type: Literal["Link"] = "Link"
    url: str
    start_idx: int
    stop_idx: int


class Reference(JurModel):
    type: Literal["Reference"] = "Reference"
    text: str
    url: str


class TextSpan(JurModel):
    type: Literal["TextSpan"] = "TextSpan"
    text: str
    links: Optional[List[Link]] = None

class Sublitera(JurModel):
    type: Literal["SubLitera"] = "SubLitera"
    ordinal: Optional[str] = None
    content: Optional[List[TextSpan]] = None


class Litera(JurModel):
    type: Literal["Litera"] = "Litera"
    ordinal: Optional[str] = None
    content: Optional[List[Annotated[Union[TextSpan, Sublitera], Field(discriminator="type")]]] = None


class Enumeration(JurModel):
    type: Literal["Enumeration"] = "Enumeration"
    ordinal: Optional[str]
    content: Optional[List[Annotated[Union[TextSpan, Reference, Litera], Field(discriminator="type")]]] = None
    references: Optional[List[Reference]] = None


class Sentence(JurModel):
    type: Literal["Sentence"] = "Sentence"
    ordinal: Optional[str] = None
    content: Optional[List[Annotated[Union[TextSpan, Reference, Enumeration], Field(discriminator="type")]]] = None
    references: Optional[List[Reference]] = None


class Section(JurModel):
    type: Literal["Section"] = "Section"
    ordinal: Optional[str] = None
    content: Optional[List[Annotated[Union[TextSpan, Reference, Sentence, Enumeration], Field(discriminator="type")]]] = None
    references: Optional[List[Reference]] = None


class Paragraph(JurModel):
    type: Literal["Paragraph"] = "Paragraph"
    ordinal: Optional[str] = None
    title: str = ""
    content: Optional[List[Annotated[Union[TextSpan, Reference, Sentence, Enumeration, Section], Field(discriminator="type")]]] = None


class Area(JurModel):
    type: Literal["Area"] = "Area"
    title: str = ""
    ordinal: Optional[str] = None
    content: Optional[List[Paragraph]] = None

    def to_text(self):
        return "".join([x.to_text() for x in self.content])


class Law(JurModel):
    type: Literal["Law"] = "Law"
    longname: Optional[str] = None
    title: str = ""
    abbreviation: str
    stemmedabbreviation:str
    content: Optional[List[Annotated[Union[Paragraph, Area], Field(discriminator="type")]]] = None

    def __int__(self, *args, **kwargs):
        self.tag = self.parent_id + "-" + self.abbreviation
        super().__init__(*args, **kwargs)

    @property
    def id(self):
        return self.parent_id + "-" + self.abbreviation

    def to_text(self):
        return "".join([x.to_text() for x in self.content])


Law.model_rebuild()
