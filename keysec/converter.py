#!/usr/bin/env python3
# encoding:utf-8


from typing import Union

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat, PublicFormat

_transform = {
    PrivateFormat.PKCS8: PrivateFormat.OpenSSH,
    PrivateFormat.OpenSSH: PrivateFormat.PKCS8,
    PublicFormat.SubjectPublicKeyInfo: PublicFormat.OpenSSH,
    PublicFormat.OpenSSH: PublicFormat.SubjectPublicKeyInfo,
}


def convert(key: Union[Ed25519PrivateKey, Ed25519PublicKey, RSAPrivateKey, RSAPublicKey], orig_format: Union[PrivateFormat, PublicFormat]) -> str:
    dst_format = _transform[orig_format]
    encoding = Encoding.OpenSSH if dst_format is PublicFormat.OpenSSH else Encoding.PEM
    if isinstance(dst_format, PrivateFormat):
        new_key = key.private_bytes(encoding=encoding, format=dst_format, encryption_algorithm=NoEncryption())
    else:
        new_key = key.public_bytes(encoding=encoding, format=dst_format)
        new_key += b'\n' if encoding is Encoding.OpenSSH else b''
    return new_key.decode('utf-8')
