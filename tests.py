import pytest

from app.main import _parse, parse_deep_limit
from app.exceptions import ParsingDeepLimitError


def test_get_root():

    et = _parse('./test.xml')

    assert et.getroot().tag == 'data'


def test_root_attr_empty():
    et = _parse('./test.xml')

    assert isinstance(et.getroot().attrib, dict)
    assert len(et.getroot().attrib.keys()) == 0


def test_parsing_deep_raises_deep_limit_error():

    et = _parse('./test.xml')

    with pytest.raises(ParsingDeepLimitError):
        parse_deep_limit(et, tag='country', limit=0)


def test_parsing_deep_find_rank():

    et = _parse('./test.xml')

    ranks = parse_deep_limit(et, 'rank')

    print(ranks)
