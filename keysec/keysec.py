#!/usr/bin/env python3
# encoding:utf-8


from keysec.converter import convert
from keysec.generator import gen_private, gen_public
from keysec.info import info
from keysec.iokeys import full_process, generate_and_write
from keysec.parser import ARGS, generate_parser, parser, parse_args


def main():
    parse_args()
    if ARGS.GENERATE:
        if ARGS.PRIVATE:
            generate_and_write(output=ARGS.OUT, func=gen_private, algorithm=ARGS.ALGORITHM, dst_format=ARGS.FORMAT, bits=ARGS.BITS)
        elif ARGS.PUBLIC:
            full_process(key=ARGS.IN, output=ARGS.OUT, func=gen_public)
        else:
            generate_parser.print_help()
    elif ARGS.CONVERT:
        full_process(key=ARGS.IN, output=ARGS.OUT, func=convert)
    elif ARGS.INFO:
        full_process(key=ARGS.IN, output=ARGS.OUT, func=info)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
