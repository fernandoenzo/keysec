#!/usr/bin/env python3
# encoding:utf-8


from argparse import ArgumentParser

from keysec.parsers.utils import CustomArgumentFormatter
from keysec.version import version_msg

top_parser = ArgumentParser(prog='keysec', description='With this program you will be able to generate OpenSSL and OpenSSH keys (RSA, Ed25519) and carry out '
                                                       'transformations between both formats.', formatter_class=CustomArgumentFormatter)

top_parser.add_argument('--version', '-v', help='print version information and exit', action='version', version=version_msg)

subparsers = top_parser.add_subparsers(dest='opt')
