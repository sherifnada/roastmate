import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union


class CmdType(Enum):
    CallMe = 'call me'


@dataclass
class CmdCallMe:
    cmd_type = CmdType.CallMe
    name: str


def is_cmd(text: str) -> bool:
    return text.lower().startswith("roastmate please")


def parse_cmd(text: str) -> Optional[Union[CmdCallMe]]:
    pattern = re.compile(r"(?i)roastmate\splease\s+((?P<cmd>call me)\s+(?P<name>.+))", re.IGNORECASE)
    match = pattern.match(text)
    if match:
        args = match.groupdict()
        cmd = match['cmd']
        if cmd == CmdType.CallMe.value:
            return CmdCallMe(match['name'])
