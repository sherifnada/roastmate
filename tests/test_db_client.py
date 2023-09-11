import pytest

from roastmate.db_client import parse_db_creds_from_url


@pytest.mark.parametrize("url, expected", [
    ("postgresql://username:password123@localhost:5432/mydb",
     {'port': '5432', 'host': 'localhost', 'user': 'username', 'password': 'password123', 'database': 'mydb'}),
    ("postgres://aoisdhoqwhie:herpderpslurp@ec2-1-234-567-890.compute-2.amazonaws.com:5432/humptydumpty",
     {'port': '5432', 'host': 'ec2-1-234-567-890.compute-2.amazonaws.com', 'user': 'aoisdhoqwhie', 'password': 'herpderpslurp',
      'database': 'humptydumpty'})
])
def test__parse_db_creds_from_url(url, expected):
    actual = parse_db_creds_from_url(url)
    assert expected == actual
