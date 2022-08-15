#!/usr/bin/env python3
# encoding:utf-8


import sys
from argparse import FileType

from keysec.parsers.top_parser import subparsers
from keysec.parsers.utils import CustomArgumentFormatter, sort_argparse_help

convert_parser = subparsers.add_parser('conv', help='transform a key from one format to another (openssl ↔ openssh)', formatter_class=CustomArgumentFormatter)
in_arg = convert_parser.add_argument('--in', '-i', metavar='key', dest='infile', nargs='?', default=sys.stdin, type=FileType('r', encoding='utf-8'),
                                     help='path to an existing PEM encoded public or private key. If not specified, it will be read from stdin')
convert_parser.add_argument('--out', '-o', metavar='filename', dest='outfile', nargs='?', default=sys.stdout, type=FileType('w', encoding='utf-8'),
                            help='output the key to the specified file. If this argument is not specified then standard output is used')
convert_parser.add_argument('--nopass', '-np', dest='nopass', action='store_true', default=False,
                            help="if this option is specified and the input key has a passphrase, the output key will not. Otherwise, the same passphrase will be kept for the output key")

sort_argparse_help(convert_parser)
