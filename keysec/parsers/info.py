#!/usr/bin/env python3
# encoding:utf-8


import sys
from argparse import FileType

from keysec.parsers.top import subparsers
from keysec.parsers.utils import CustomArgumentFormatter, sort_argparse_help

info_parser = subparsers.add_parser('info', help='show information about a key', formatter_class=CustomArgumentFormatter)
info_parser.add_argument('--in', '-i', metavar='key', dest='infile', nargs='?', default=sys.stdin, type=FileType('r', encoding='utf-8'),
                         help='path to an existing PEM encoded public or private key. If not specified, it will be read from stdin')
info_parser.add_argument('--out', '-o', metavar='filename', dest='outfile', nargs='?', default=sys.stdout, type=FileType('w', encoding='utf-8'),
                         help='output the information to the specified file. If this argument is not specified then standard output is used')

sort_argparse_help(info_parser)
