#!/usr/bin/env python3
# encoding:utf-8


import sys
from argparse import FileType

from keysec.parsers.top_parser import subparsers
from keysec.parsers.utils import CustomArgumentFormatter, sort_argparse_help

edit_parser = subparsers.add_parser('edit', help='edit the passphrase and comment of a key', formatter_class=CustomArgumentFormatter)
edit_parser.add_argument('--in', '-i', metavar='key', dest='infile', nargs='?', default=sys.stdin, type=FileType('r', encoding='utf-8'),
                         help='path to an existing PEM encoded public or private key. If not specified, it will be read from stdin')
edit_parser.add_argument('--out', '-o', metavar='filename', dest='outfile', nargs='?', default=sys.stdout, type=FileType('w', encoding='utf-8'),
                         help='output the key to the specified file. If this argument is not specified then standard output is used')
edit_parser.add_argument('--pass', '-p', action='store_true', help='interactively set/edit the key passphrase')
edit_parser.add_argument('--comment', '-c', metavar='comment', nargs='?', const=True, default=None,
                         help='set/edit the key comment (only OpenSSH format). If this option is specified but not followed by a comment, '
                              'then an input is prompted to enter the comment interactively')

sort_argparse_help(edit_parser)
