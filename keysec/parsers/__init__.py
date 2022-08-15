#!/usr/bin/env python3
# encoding:utf-8


from keysec.parsers import top_parser, gen_parser, conv_parser, edit_parser, info_parser

from keysec.parsers.conv_parser import in_arg
from keysec.parsers.gen_parser import generate_parser
from keysec.parsers.top_parser import ARGS, parse_args, sort_argparse_help, top_parser, subparsers

sort_argparse_help(subparsers)
sort_argparse_help(top_parser)
