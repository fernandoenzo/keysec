#!/usr/bin/env python3
# encoding:utf-8


from argparse import ArgumentError
from typing import Type, Union

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import PrivateFormat, PublicFormat

from keysec.iokeys import key_to_str
from keysec.parser import in_arg


def gen_private(algorithm: Type[Union[Ed25519PrivateKey, RSAPrivateKey]], dst_format: PrivateFormat, bits: int = None) -> str:
    key = rsa.generate_private_key(public_exponent=65537, key_size=bits) if algorithm is RSAPrivateKey else Ed25519PrivateKey.generate()
    return key_to_str(key=key, str_format=dst_format)


def gen_public(priv_key: Union[Ed25519PrivateKey, RSAPrivateKey], orig_format: PrivateFormat, comment: str) -> str:
    if not isinstance(orig_format, PrivateFormat):
        raise ArgumentError(argument=in_arg, message='specified key is not private')
    dst_format = PublicFormat.OpenSSH if orig_format is PrivateFormat.OpenSSH else PublicFormat.SubjectPublicKeyInfo
    pub_key = priv_key.public_key()
    return key_to_str(key=pub_key, str_format=dst_format)
