#!/usr/bin/env python3
# encoding:utf-8


import subprocess
from typing import Union

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat

from keysec.converter import convert
from keysec.iokeys import load_and_process


def ed25519() -> str:
    res = subprocess.run(['openssl', 'genpkey', '-algorithm', 'ED25519'], capture_output=True, text=True, check=True)
    return res.stdout


def rsa(bits: int) -> str:
    res = subprocess.run(['openssl', 'genpkey', '-algorithm', 'RSA', '-pkeyopt', f'rsa_keygen_bits:{bits}'], capture_output=True, text=True, check=True)
    return res.stdout


def ed25519_ssh() -> str:
    return load_and_process(key=ed25519(), func=convert)


def rsa_ssh(bits: int) -> str:
    return load_and_process(key=rsa(bits), func=convert)


def gen_private(algorithm: str, dst_format: str, bits: int = None) -> str:
    key = None
    if algorithm == 'ed25519' and dst_format == 'openssl':
        key = ed25519()
    elif algorithm == 'ed25519' and dst_format == 'openssh':
        key = ed25519_ssh()
    elif algorithm == 'rsa' and dst_format == 'openssl':
        key = rsa(bits)
    elif algorithm == 'rsa' and dst_format == 'openssh':
        key = rsa_ssh(bits)
    return key


def gen_public(priv_key: Union[Ed25519PrivateKey, RSAPrivateKey], orig_format: PrivateFormat) -> str:
    if not isinstance(orig_format, PrivateFormat):
        raise ValueError('The specified key is not private')
    dst_format = PublicFormat.OpenSSH if orig_format is PrivateFormat.OpenSSH else PublicFormat.SubjectPublicKeyInfo
    encoding = Encoding.OpenSSH if dst_format is PublicFormat.OpenSSH else Encoding.PEM
    pub_key = priv_key.public_key()
    pub_key = pub_key.public_bytes(encoding=encoding, format=dst_format)
    pub_key += b'\n' if encoding is Encoding.OpenSSH else b''
    return pub_key.decode('utf-8')
