import pytest

from app.main import my_parse, parse_deep_limit
from app.exceptions import ParsingDeepLimitError, ExecutionTimeLimitError


def test_get_root():

    et = my_parse('./test.xml')

    assert et.getroot().tag == 'data'


def test_root_attr_empty():
    et = my_parse('./test.xml')

    assert isinstance(et.getroot().attrib, dict)
    assert len(et.getroot().attrib.keys()) == 0


def test_parsing_deep_raises_deep_limit_error():

    et = my_parse('./test.xml')

    with pytest.raises(ParsingDeepLimitError):
        parse_deep_limit(et, tag='country', limit=0)


def test_parsing_deep_find_rank():

    et = my_parse('./test.xml')

    ranks = parse_deep_limit(et, 'rank', limit=5)

    assert len(ranks) == 5


def test_parsing_deep_time_limit_error():

    with pytest.raises(ExecutionTimeLimitError):
        my_parse(file='test.xml', tag='rank', time_limit=1)
