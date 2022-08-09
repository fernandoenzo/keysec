#!/usr/bin/env python3
# encoding:utf-8


import collections
import os
import sys
import textwrap
from argparse import ArgumentParser, RawTextHelpFormatter, ArgumentTypeError, FileType

os.umask(0o177)  # chmod 600


class ARGS:
    ALGORITHM = None
    BITS = None
    CONVERT = None
    FORMAT = None
    GENERATE = None
    IN = None
    INFO = None
    OUT = None
    PRIVATE = None
    PUBLIC = None


class CustomArgumentFormatter(RawTextHelpFormatter):
    # https://stackoverflow.com/a/65891304
    """Formats argument help which maintains line length restrictions as well as appends default value if present."""

    def _split_lines(self, text, width):
        text = super()._split_lines(text, width)
        new_text = []

        # loop through all the lines to create the correct wrapping for each line segment.
        for line in text:
            if not line:
                # this would be a new line.
                new_text.append(line)
                continue

            # wrap the line's help segment which preserves new lines but ensures line lengths are
            # honored
            new_text.extend(textwrap.wrap(line, width))

        return new_text


def check_positive(value) -> int:
    try:
        value = int(value)
        if value < 0:
            raise ValueError
    except:
        raise ArgumentTypeError(f'key size {value} must be a positive integer')
    return value


def sort_argparse_help(parser: ArgumentParser):
    for g in parser._action_groups:
        g._group_actions.sort(key=lambda x: x.dest)


parser = ArgumentParser(prog='keysec', description='With this program you will be able to generate OpenSSL and OpenSSH keys (RSA, Ed25519) and carry out '
                                                   'transformations between both formats.', formatter_class=CustomArgumentFormatter)

subparsers = parser.add_subparsers(dest='opt')

# Generate a new key pair
generate_parser = subparsers.add_parser('gen', help='generate a brand new key pair', formatter_class=CustomArgumentFormatter)
generate_subparser = generate_parser.add_subparsers(dest='gen')

# Generate a private key
private_parser = generate_subparser.add_parser('priv', help='generate a private key in the specified format', formatter_class=CustomArgumentFormatter)
private_parser.add_argument('--algo', '-a', dest='algorithm', choices=['rsa', 'ed25519'], default='ed25519',
                            help='which algorithm should use the generated key. If this argument is not specified, then Ed25519 is used')
private_parser.add_argument('--bits', '-b', choices=['2048', '4096'], default='2048',
                            help='RSA key size if chosen. Ed25519 works exclusively with 256-bit keys')
private_parser.add_argument('--out', '-o', metavar='filename', dest='outfile', nargs='?', default=sys.stdout, type=FileType('w', encoding='utf-8'),
                            help='output the key to the specified file. If this argument is not specified then standard output is used')
private_parser.add_argument('--format', '-f', choices=['openssl', 'openssh'], default='openssl',
                            help='format of the generated key. If this argument is not specified then OpenSSL is used')

# Generate a public key
public_parser = generate_subparser.add_parser('pub', help='given a private key, generate its associated public key with the same format', formatter_class=CustomArgumentFormatter)
public_parser.add_argument('--in', '-i', metavar='private-key', dest='infile', nargs='?', default=sys.stdin, type=FileType('r', encoding='utf-8'),
                           help='path to an existing PEM encoded private key. If not specified, it will be read from stdin.')
public_parser.add_argument('--out', '-o', metavar='filename', dest='outfile', nargs='?', default=sys.stdout, type=FileType('w', encoding='utf-8'),
                           help='output the key to the specified file. If this argument is not specified then standard output is used')

# Convert between key formats
convert_parser = subparsers.add_parser('conv', help='transform a key from one format to another (openssl ↔ openssh)', formatter_class=CustomArgumentFormatter)
convert_parser.add_argument('--in', '-i', metavar='key', dest='infile', nargs='?', default=sys.stdin, type=FileType('r', encoding='utf-8'),
                            help='path to an existing PEM encoded public or private key. If not specified, it will be read from stdin.')
convert_parser.add_argument('--out', '-o', metavar='filename', dest='outfile', nargs='?', default=sys.stdout, type=FileType('w', encoding='utf-8'),
                            help='output the key to the specified file. If this argument is not specified then standard output is used')

# See information about a key
info_parser = subparsers.add_parser('info', help='show information about a key')
info_parser.add_argument('--in', '-i', metavar='key', dest='infile', nargs='?', default=sys.stdin, type=FileType('r', encoding='utf-8'),
                         help='path to an existing PEM encoded public or private key. If not specified, it will be read from stdin.')
info_parser.add_argument('--out', '-o', metavar='filename', dest='outfile', nargs='?', default=sys.stdout, type=FileType('w', encoding='utf-8'),
                         help='output the information to the specified file. If this argument is not specified then standard output is used')

collections.deque((sort_argparse_help(p) for p in (parser, generate_parser, private_parser, public_parser, convert_parser, info_parser)), maxlen=0)


def parse_args():
    args = vars(parser.parse_args())
    ARGS.ALGORITHM = args.get('algorithm')
    ARGS.BITS = args.get('bits')
    ARGS.FORMAT = args.get('format')
    ARGS.IN = args.get('infile')
    ARGS.OUT = args.get('outfile')
    ARGS.CONVERT = True if args.get('opt') == 'conv' else None
    ARGS.GENERATE = True if args.get('opt') == 'gen' else None
    ARGS.INFO = True if args.get('opt') == 'info' else None
    ARGS.PRIVATE = True if args.get('gen') == 'priv' else None
    ARGS.PUBLIC = True if args.get('gen') == 'pub' else None
    return args
