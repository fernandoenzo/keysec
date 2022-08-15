#!/usr/bin/env python3
# encoding:utf-8


import os
import sys

from keysec.actions import convert, edit, gen_private, gen_public, info
from keysec.iokeys import full_process, generate_and_write
from keysec.parsers import ARGS, generate_parser, parse_args, top_parser

sys.tracebacklimit = 0

os.umask(0o177)  # chmod 600


def main():
    parse_args()
    if ARGS.GENERATE:
        if ARGS.PRIVATE:
            generate_and_write(output=ARGS.OUT, func=gen_private, algorithm=ARGS.ALGORITHM, dst_format=ARGS.FORMAT, bits=ARGS.BITS)
        elif ARGS.PUBLIC:
            full_process(key_str=ARGS.IN, output=ARGS.OUT, func=gen_public)
        else:
            generate_parser.print_help()
    elif ARGS.CONVERT:
        full_process(key_str=ARGS.IN, output=ARGS.OUT, func=convert, nopass=ARGS.NOPASS)
    elif ARGS.EDIT:
        full_process(key_str=ARGS.IN, output=ARGS.OUT, func=edit, comment=ARGS.COMMENT, password=ARGS.PASSWORD)
    elif ARGS.INFO:
        full_process(key_str=ARGS.IN, output=ARGS.OUT, func=info)
    else:
        top_parser.print_help()


if __name__ == '__main__':
    main()
