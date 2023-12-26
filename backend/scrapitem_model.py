from pydantic import BaseModel
from datetime import datetime

from pydantic.class_validators import Optional

from law_model import Law


class ScrapItem(BaseModel):
    url: str
    date: datetime
    html: str
