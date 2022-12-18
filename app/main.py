import os
import sys
import argparse
import datetime
import queue
import defusedxml

from defusedxml.ElementTree import parse

import app.settings as settings
from app.exceptions import ParsingDeepLimitError, WrongFileExtensionError, FilesizeLimitError, ExecutionTimeLimitError


def get_cli_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('file', help='XML file to parse')
    parser.add_argument('-collect_text', help='Collect text from tag', type=bool, default=True)
    parser.add_argument('-collect_attrib', help='Collect attributes from tag', type=bool, default=False)
    parser.add_argument('-tag', help='Tag to collect', type=str, default='root')
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


def parse_deep_limit(tree: defusedxml.ElementTree, tag='root', limit=settings.LDEEP, time_limit=settings.LTIME,
                     collect_text=True, collect_attrib=False):
    """

    :param tree:
    :param tag:
    :param limit:
    :param time_limit:
    :param collect_text:
    :raises ParsingDeepLimitError, ExecutionTimeLimitError
    :return:
    """

    start = datetime.datetime.now()

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

        if str.lower(el[1].tag) == str.lower(tag):

            data = dict()

            data['tag'] = el[1].tag

            if collect_text:
                data['text'] = str.strip(el[1].text if el[1].text is not None else '')

            if collect_attrib:
                data['attrib'] = el[1].attrib

            result.append(data)

        for child in el[1]:
            q.put((deep + 1, child))

        if (datetime.datetime.now() - start).seconds > time_limit:
            raise ExecutionTimeLimitError(f'You reached time limit which is {time_limit} seconds')

    return result


def my_parse(file, tag='root', forbid_dtd=settings.DTD, forbid_entities=settings.EEXPAND,
             forbid_external=settings.EEROSLVE, deep=settings.LDEEP, time_limit=settings.LTIME):

    tree = parse(file, forbid_dtd=forbid_dtd, forbid_entities=forbid_entities, forbid_external=forbid_external)

    return parse_deep_limit(tree, tag, limit=deep, time_limit=time_limit)


def main():

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

    try:
        parsed = my_parse(cli_args.file, tag=cli_args.tag, forbid_dtd=cli_args.dtd, forbid_entities=cli_args.eexpand, forbid_external=cli_args.eresolve, deep=settings.LDEEP, time_limit=settings.LTIME)
        print(parsed)
    except Exception as e:
        print(e)
        sys.exit(1)
