#!/usr/bin/env python3
# encoding:utf-8


from typing import Union

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat


def convert(priv_key: Union[Ed25519PrivateKey, RSAPrivateKey], orig_format: PrivateFormat) -> str:
    dst_format = PrivateFormat.OpenSSH if orig_format is PrivateFormat.PKCS8 else PrivateFormat.PKCS8
    new_key = priv_key.private_bytes(encoding=Encoding.PEM, format=dst_format, encryption_algorithm=NoEncryption())
    return new_key.decode('utf-8')
