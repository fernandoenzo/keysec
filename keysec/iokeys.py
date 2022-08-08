#!/usr/bin/env python3
# encoding:utf-8


from io import TextIOWrapper
from typing import Union, Callable, Tuple

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_ssh_private_key, PrivateFormat


def read_key(priv_key: TextIOWrapper) -> str:
    return priv_key.read()


def load_priv_key(priv_key: str) -> Tuple[Union[Ed25519PrivateKey, RSAPrivateKey], PrivateFormat]:
    priv_key: bytes = priv_key.encode('utf-8')
    loaded_key = None
    funcs = ((load_pem_private_key, PrivateFormat.PKCS8), (load_ssh_private_key, PrivateFormat.OpenSSH))
    for load in funcs:
        try:
            loaded_key = load[0](priv_key, password=None)
            break
        except:
            pass
    if loaded_key is None:
        raise ValueError('The specified key is not in OpenSSL PEM nor OpenSSH format')
    return loaded_key, load[1]


def write_key(key: str, output: TextIOWrapper):
    output.write(key)
    output.flush()
    if not output.name == '<stdout>':
        output.close()


def generate_and_write(output: TextIOWrapper, func: Callable[..., str], *args, **kwargs):
    key = func(*args, **kwargs)
    write_key(key=key, output=output)


def load_and_process(priv_key: str, func: Callable[[Union[Ed25519PrivateKey, RSAPrivateKey], PrivateFormat, ...], str], *args, **kwargs) -> str:
    priv_key = load_priv_key(priv_key=priv_key)
    priv_key, orig_format = priv_key[0], priv_key[1]
    return func(priv_key, orig_format, *args, **kwargs)


def load_process_and_write(priv_key: str, output: TextIOWrapper, func: Callable[[Union[Ed25519PrivateKey, RSAPrivateKey], ...], str], *args, **kwargs):
    key = load_and_process(priv_key=priv_key, func=func, *args, **kwargs)
    write_key(key=key, output=output)


def full_process(priv_key: TextIOWrapper, output: TextIOWrapper, func: Callable[[Union[Ed25519PrivateKey, RSAPrivateKey], ...], str], *args, **kwargs):
    priv_key: str = read_key(priv_key)
    load_process_and_write(priv_key=priv_key, output=output, func=func, *args, **kwargs)
