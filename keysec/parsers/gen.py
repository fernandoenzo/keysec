#!/usr/bin/env python3
# encoding:utf-8


import collections
import sys
from argparse import Action, FileType

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import PrivateFormat

from keysec.parsers.top import subparsers
from keysec.parsers.utils import CustomArgumentFormatter, sort_argparse_help


class AlgorithmAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        algo = RSAPrivateKey if values == 'rsa' else Ed25519PrivateKey
        setattr(namespace, self.dest, algo)


class FormatAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        dst_format = PrivateFormat.OpenSSH if values == 'openssh' else PrivateFormat.PKCS8
        setattr(namespace, self.dest, dst_format)


generate_parser = subparsers.add_parser('gen', help='generate a brand new key pair', formatter_class=CustomArgumentFormatter)
generate_subparser = generate_parser.add_subparsers(dest='gen')

# Generate a private key
private_parser = generate_subparser.add_parser('priv', help='generate a private key in the specified format', formatter_class=CustomArgumentFormatter)
private_parser.add_argument('--algo', '-a', dest='algorithm', type=str.lower, choices=['rsa', 'ed25519'], default=Ed25519PrivateKey, action=AlgorithmAction,
                            help='which algorithm should use the generated key. If this argument is not specified, then Ed25519 is used')
private_parser.add_argument('--bits', '-b', type=int, choices=[2048, 4096], default=2048,
                            help='RSA key size if chosen. Ed25519 works exclusively with 256-bit keys')
private_parser.add_argument('--out', '-o', metavar='filename', dest='outfile', nargs='?', default=sys.stdout, type=FileType('w', encoding='utf-8'),
                            help='output the key to the specified file. If this argument is not specified then standard output is used')
private_parser.add_argument('--format', '-f', choices=['openssl', 'openssh'], default=PrivateFormat.PKCS8, action=FormatAction,
                            help='format of the generated key. If this argument is not specified then OpenSSL is used')

# Generate a public key
public_parser = generate_subparser.add_parser('pub', help='given a private key, generate its associated public key with the same format', formatter_class=CustomArgumentFormatter)
public_parser.add_argument('--in', '-i', metavar='private-key', dest='infile', nargs='?', default=sys.stdin, type=FileType('r', encoding='utf-8'),
                           help='path to an existing PEM encoded private key. If not specified, it will be read from stdin')
public_parser.add_argument('--out', '-o', metavar='filename', dest='outfile', nargs='?', default=sys.stdout, type=FileType('w', encoding='utf-8'),
                           help='output the key to the specified file. If this argument is not specified then standard output is used')

collections.deque((sort_argparse_help(p) for p in (generate_parser, generate_subparser, private_parser, public_parser)), maxlen=0)
