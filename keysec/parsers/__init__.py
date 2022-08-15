#!/usr/bin/env python3
# encoding:utf-8


from keysec.parsers import top, gen, conv, edit, info
from keysec.parsers.args import ARGS, parse_args
from keysec.parsers.conv import in_arg
from keysec.parsers.gen import generate_parser
from keysec.parsers.top import subparsers, top_parser
from keysec.parsers.utils import sort_argparse_help

sort_argparse_help(subparsers)
sort_argparse_help(top_parser)
