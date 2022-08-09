#!/usr/bin/env python3
# encoding:utf-8


from typing import Union

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.serialization import PrivateFormat, PublicFormat

from keysec.iokeys import key_to_str

_transform = {
    PrivateFormat.PKCS8: PrivateFormat.OpenSSH,
    PrivateFormat.OpenSSH: PrivateFormat.PKCS8,
    PublicFormat.SubjectPublicKeyInfo: PublicFormat.OpenSSH,
    PublicFormat.OpenSSH: PublicFormat.SubjectPublicKeyInfo,
}


def convert(key: Union[Ed25519PrivateKey, Ed25519PublicKey, RSAPrivateKey, RSAPublicKey], orig_format: Union[PrivateFormat, PublicFormat]) -> str:
    dst_format = _transform[orig_format]
    return key_to_str(key=key, str_format=dst_format)
