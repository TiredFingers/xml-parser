import argparse


parser = argparse.ArgumentParser()


def setup():
    _setup_argparse()
    args = parser.parse_args()


def _setup_argparse():
    parser.add_argument('file', help='XML file to parse')
    parser.add_argument('--dtd', help='Prohibit DTD')
    parser.add_argument('--eexpand', help='Allow entities expand')
    parser.add_argument('--eresolve', help='Allow external resolve')
    parser.add_argument('--ldeep', help='Limit deep of parsing')
    parser.add_argument('--lsize', help='Limit size of input file')
    parser.add_argument('--ltime', help='Limit time of parsing')

