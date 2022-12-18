import os
import sys
import argparse
import defusedxml

from defusedxml.ElementTree import parse

import app.settings as settings
from app.exceptions import ParsingDeepLimitError, WrongFileExtensionError, FilesizeLimitError


def get_cli_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('file', help='XML file to parse')
    parser.add_argument('-dtd', help='Prohibit DTD', choices=[True, False], type=bool, default=settings.DTD)
    parser.add_argument('-eexpand', help='Allow entities expand', choices=[True, False], type=bool,
                        default=settings.EEXPAND)
    parser.add_argument('-eresolve', help='Allow external resolve', choices=[True, False], type=bool,
                        default=settings.EEROSLVE)
    parser.add_argument('-ldeep', help='Limit deep of parsing', choices=[True, False], type=bool,
                        default=settings.LDEEP)
    parser.add_argument('-lsize', help='Limit size of input file Mb', choices=[True, False], type=bool,
                        default=settings.LSIZE)
    parser.add_argument('-ltime', help='Limit time of parsing', choices=[True, False], type=bool,
                        default=settings.LTIME)

    return parser.parse_args()


def parse_deep_limit(tree: defusedxml.ElementTree, tag='root', limit=settings.LDEEP):
    """

    :param tree:
    :param tag:
    :param limit:
    :return:
    :raises: ParsingDeepLimitError
    """

    import queue

    if tag == 'root':
        return tree.getroot()

    root = tree.getroot()

    q = queue.LifoQueue()

    q.put((0, root))
    result = list()

    while not q.empty():

        el = q.get()

        deep = el[0]

        if deep >= limit:
            raise ParsingDeepLimitError(f'You reached deep limit {limit}')

        if el[1].tag == tag:
            result.append(str.strip(el[1].text))

        for child in el[1]:
            q.put((deep + 1, child))

    return result


def my_parse(file, tag='root', forbid_dtd=settings.DTD, forbid_entities=settings.EEXPAND,
             forbid_external=settings.EEROSLVE, deep=settings.LDEEP, time_limit=settings.LTIME):

    tree = parse(file, forbid_dtd=forbid_dtd, forbid_entities=forbid_entities, forbid_external=forbid_external)

    return parse_deep_limit(tree, tag, limit=deep)


def main():
    # todo
    # время парсинга

    cli_args = get_cli_args()

    try:

        if os.path.splitext(cli_args.file)[1] != '.xml':
            raise WrongFileExtensionError(f'Bad file extension. Can only be .xml')

    except WrongFileExtensionError as e:
        print(e)
        sys.exit(1)

    try:
        if not os.path.isfile(os.path.abspath(cli_args.file)):
            raise Exception(f'{cli_args.file} is not a file')
    except Exception as e:
        print(e)
        sys.exit(1)

    try:
        if os.stat(cli_args.file).st_size / (1024 * 1024) > settings.LSIZE:
            raise FilesizeLimitError(f'File too big. Limit is {settings.LSIZE} Mb')
    except FilesizeLimitError as e:
        print(e)
        sys.exit(1)

    parsed = my_parse(cli_args.file, forbid_dtd=cli_args.dtd, forbid_entities=cli_args.eexpand, forbid_external=cli_args.eresolve, deep=settings.LDEEP, time_limit=settings.LTIME)
