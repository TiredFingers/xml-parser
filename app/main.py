import argparse
import settings

from defusedxml.ElementTree import parse


def get_cli_args():

    parser = argparse.ArgumentParser()

    parser.add_argument('file', help='XML file to parse')
    parser.add_argument('-dtd', help='Prohibit DTD', choices=[True, False], type=bool, default=settings.DTD)
    parser.add_argument('-eexpand', help='Allow entities expand', choices=[True, False], type=bool, default=settings.EEXPAND)
    parser.add_argument('-eresolve', help='Allow external resolve', choices=[True, False], type=bool, default=settings.EEROSLVE)
    parser.add_argument('-ldeep', help='Limit deep of parsing', choices=[True, False], type=bool, default=settings.LDEEP)
    parser.add_argument('-lsize', help='Limit size of input file Mb', choices=[True, False], type=bool, default=settings.LSIZE)
    parser.add_argument('-ltime', help='Limit time of parsing', choices=[True, False], type=bool, default=settings.LTIME)

    return parser.parse_args()


def _parse(file, forbid_dtd, forbid_entities, forbid_external, deep, file_size_limit, time_limit):

    return parse(file, forbid_dtd=forbid_dtd, forbid_entities=forbid_entities, forbid_external=forbid_external)


def main():
    # todo
    # глубина парсинга
    # размер входящего файла
    # время парсинга

    cli_args = get_cli_args()
    parsed = _parse(cli_args.file, forbid_dtd=cli_args.dtd, forbid_entities=cli_args.eexpand,
                    forbid_external=cli_args.eresolve, deep=settings.LDEEP,
                    file_size_limit=settings.LSIZE, time_limit=settings.LTIME)


