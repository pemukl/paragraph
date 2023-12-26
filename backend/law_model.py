from __future__ import annotations
import json
import logging
from abc import ABC, abstractmethod

from typing import List, Optional, Union, Any, Dict
import re

from pydantic import BaseModel, Field
from pydantic.class_validators import Tuple
from pydantic.typing import Literal

class BaseModel(BaseModel,ABC):
    parent_id: str
    tag: Optional[str]


    @property
    def id(self):
        if self.tag is not None:
            if self.ordinal is not None:
                return self.parent_id+"-"+self.tag+str(self.ordinal)
            elif hasattr(self, "title") and self.title is not None:
                return self.parent_id+"-"+self.tag+self.title
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
            logging.warning("no text found in "+str(self))

    def get_textspans(self):
        """get all textspans from content"""
        if(isinstance(self,TextSpan)):
            yield self
        if(hasattr(self,"content")):
            if(isinstance(self.content,list)):
                for x in self.content:
                    yield from x.get_textspans()

class Link(BaseModel):
    type: Literal["Link"] = "Link"
    url: str
    start_idx: str
    stop_idx: str

class Reference(BaseModel):
    type: Literal["Reference"] = "Reference"
    text: str
    url: str


class TextSpan(BaseModel):
    type: Literal["TextSpan"] = "TextSpan"
    text: str
    links: Optional[List[Link]]


class Sublitera(BaseModel):
    tag = Field("SubLit", exclude=True)
    type: Literal["Litera"] = "Sublitera"
    ordinal: Optional[str] = None
    content: Optional[List[TextSpan]] = None


class Litera(BaseModel):
    tag = Field("Lit", exclude=True)
    type: Literal["Litera"] = "Litera"
    ordinal: Optional[str] = None
    content: Optional[List[Union[TextSpan, Sublitera]]]



class Dummy(BaseModel):
    type: str = "Dummy"
    content: Optional[Union[str,TextSpan,List[Union[TextSpan,Reference,Litera,Any]],Any]]
    ordinal: Optional[str] = None
    def __init__(self, **data: Any):
        super().__init__(**data)
        if isinstance(self.content, list):
            logging.warning('Dummy '+self.type+' '+str(self.ordinal)+' created while parsing: ' + str([x["type"] for x in self.content]))
        else:
            logging.warning('Dummy '+self.type+' created while parsing: '+str(self))

class Enumeration(BaseModel):
    tag = Field("Enum", exclude=True)
    type: Literal["Enumeration"] = "Enumeration"
    ordinal: Optional[str]
    content: Optional[List[Union[TextSpan, Reference, Litera, Dummy]]]
    references: Optional[List[Reference]]


class Sentence(BaseModel):
    tag = Field("Sent", exclude=True)
    type: Literal["Sentence"] = "Sentence"
    ordinal: Optional[str]
    content: Optional[List[Union[TextSpan, Reference, Enumeration]]]
    references: Optional[List[Reference]]


class Section(BaseModel):
    tag = Field("Sec", exclude=True)
    type: Literal["Section"] = "Section"
    ordinal: Optional[str]
    content: Optional[List[Union[TextSpan, Reference, Sentence, Enumeration, Dummy]]]
    references: Optional[List[Reference]]


class Paragraph(BaseModel):
    tag = Field("Par", exclude=True)
    type: Literal["Paragraph"] = "Paragraph"
    ordinal: Optional[str]
    title: str
    content: Optional[List[Union[TextSpan, Reference, Sentence, Enumeration, Section]]]


class Area(BaseModel):
    type: Literal["Area"] = "Area"
    title: str
    ordinal: str
    content: Optional[List[Union[Paragraph]]]

    def to_text(self):
        return "".join([x.to_text() for x in self.content])


class Law(BaseModel):
    type: Literal["Law"] = "Law"
    title: str
    abbreviation: str
    content: Optional[List[Union[Area, Paragraph]]] = None


    def __int__(self, *args, **kwargs):
        self.tag = self.parent_id + "-" + self.abbreviation
        super().__init__(*args, **kwargs)
    @property
    def id(self):
        return self.parent_id + "-" + self.abbreviation

    def to_text(self):
        return "".join([x.to_text() for x in self.content])

