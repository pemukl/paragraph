from paraback.models.law_model import JurModel
from typing import Literal

class LinkModel(JurModel):
    type: Literal["Link"] = "Link"
    url: str
    start_idx: int
    stop_idx: int

