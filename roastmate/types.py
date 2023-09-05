from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class SenderRole(Enum):
    USER = 'USER'
    LLM = 'LLM'


@dataclass
class Contact:
    first_name: str
    number: str


@dataclass
class TextMessage:
    sender_number: str
    content: str
    sender_role: SenderRole = SenderRole.USER
    date_sent: Optional[datetime] = None
    date_received: Optional[datetime] = None
    sender_name: Optional[str] = None
