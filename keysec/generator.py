#!/usr/bin/env python3
# encoding:utf-8


from argparse import ArgumentError
from typing import Type, Union

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import PrivateFormat, PublicFormat

from keysec.iokeys import Key
from keysec.parser import in_arg


def gen_private(algorithm: Type[Union[Ed25519PrivateKey, RSAPrivateKey]], dst_format: PrivateFormat, bits: int = None) -> str:
    key = Key()
    key.key = rsa.generate_private_key(public_exponent=65537, key_size=bits) if algorithm is RSAPrivateKey else Ed25519PrivateKey.generate()
    key.orig_format = PrivateFormat.PKCS8
    return key.to_str(str_format=dst_format)


def gen_public(priv_key: Key) -> str:
    if not isinstance(priv_key.orig_format, PrivateFormat):
        raise ArgumentError(argument=in_arg, message='specified key is not private')
    dst_format = PublicFormat.OpenSSH if priv_key.orig_format is PrivateFormat.OpenSSH else PublicFormat.SubjectPublicKeyInfo
    return priv_key.to_str(str_format=dst_format)
