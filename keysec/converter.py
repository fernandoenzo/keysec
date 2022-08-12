#!/usr/bin/env python3
# encoding:utf-8


from cryptography.hazmat.primitives.serialization import PrivateFormat, PublicFormat

from keysec.iokeys import Key

_transform = {
    PrivateFormat.PKCS8: PrivateFormat.OpenSSH,
    PrivateFormat.OpenSSH: PrivateFormat.PKCS8,
    PublicFormat.SubjectPublicKeyInfo: PublicFormat.OpenSSH,
    PublicFormat.OpenSSH: PublicFormat.SubjectPublicKeyInfo,
}


def convert(key: Key) -> str:
    dst_format = _transform[key.orig_format]
    return key.to_str(str_format=dst_format)
