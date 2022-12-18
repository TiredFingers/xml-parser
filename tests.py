import pytest

from app.main import my_parse, parse_deep_limit
from app.exceptions import ParsingDeepLimitError, ExecutionTimeLimitError

from defusedxml.common import DTDForbidden


def test_get_root():

    et = my_parse('./testxmldata/test.xml')

    assert et.tag == 'data'


def test_root_attr_empty():

    et = my_parse('./testxmldata/test.xml')

    assert isinstance(et.attrib, dict)
    assert len(et.attrib.keys()) == 0


def test_parsing_deep_raises_deep_limit_error():

    with pytest.raises(ParsingDeepLimitError):
        my_parse(file='./testxmldata/test.xml', tag='country', deep=0)


def test_parsing_deep_find_rank():

    ranks = my_parse(file='./testxmldata/test.xml', tag='rank', deep=5)

    assert len(ranks) == 5


def test_parsing_deep_time_limit_error():

    with pytest.raises(ExecutionTimeLimitError):
        my_parse(file='./testxmldata/test.xml', tag='rank', time_limit=float('-inf'))


def test_my_parse_cyclic_bomb():

    with pytest.raises(DTDForbidden):
        my_parse(file='./testxmldata/cyclic.xml')


def test_my_parse_dtd():

    with pytest.raises(DTDForbidden):
        my_parse(file='./testxmldata/dtd.xml')


def test_my_parse_external():

    with pytest.raises(DTDForbidden):
        my_parse(file='./testxmldata/external.xml')


def test_my_parse_external_file():

    with pytest.raises(DTDForbidden):
        my_parse(file='./testxmldata/external_file.xml')


def test_my_parse_quadratic():

    with pytest.raises(DTDForbidden):
        my_parse(file='./testxmldata/quadratic.xml')


def test_my_parse_xmlbomb():

    with pytest.raises(DTDForbidden):
        my_parse('./testxmldata/xmlbomb.xml')


def test_my_parse_xmlbomb2():

    with pytest.raises(DTDForbidden):
        my_parse('./testxmldata/xmlbomb2.xml')
