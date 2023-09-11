import pytest

from roastmate.command_parser import parse_cmd, CmdCallMe


@pytest.mark.parametrize("message, expected", [
    # Invalid formats
    ("roastmate make me a sanddwich", None),
    ("hello world", None),
    ("poop", None),
    ("roastmate is great", None),

    # Valid
    ("roastmate please call me sherif", CmdCallMe("sherif")),
    ("roastmate PLEASE call me brandon", CmdCallMe("brandon")),
    ("RoAsTmAtE PlEaSe call me Johnson", CmdCallMe("Johnson")),
    ("Roastmate please call me Earth's greatest warrior", CmdCallMe("Earth's greatest warrior")),
    ("Roastmate please call me her majesty      the queen", CmdCallMe("her majesty      the queen")),
])
def test_parse_cmd(message, expected):
    actual = parse_cmd(message)
    assert expected == actual
