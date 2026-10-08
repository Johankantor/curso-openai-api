from typing import List

from pydantic import BaseModel


class CampaignBrief(BaseModel):
    """Forma esperada de  un brief de campana (Structured Outputs.)"""

    title: str
    objective: str
    audience: List[str]
    tone: str
    channels: List[str]
    next_steps: List[str]

class ContentPiece(BaseModel):
    """Una pieza de contenido lista para publicar en un canal."""

    channel: str
    title: str
    body: str
    call_to_action:str