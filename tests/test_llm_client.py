from roastmate.llm_client import parse_api_key
import roastmate.constants as Constants
from unittest.mock import mock_open, patch


def test_parse_api_key_from_env(monkeypatch):
    expected = "api-key"
    monkeypatch.setenv(Constants.OPENAI_API_KEY, '{"api-key": "api-key"}')
    assert expected == parse_api_key()


def test_parse_api_key_from_file(monkeypatch):
    expected = "api-key"
    mock_file_path = "secrets/openai.json"
    mock_data = '{"api-key": "api-key"}'
    original_open = open

    m = mock_open(read_data=mock_data)

    def side_effect_open(path, *args, **kwargs):
        if path == mock_file_path:
            return m()
        return original_open(path, *args, **kwargs)

    with patch('builtins.open', side_effect=side_effect_open):
        assert expected == parse_api_key()
