#!/usr/bin/env python3
# encoding:utf-8


import subprocess
from argparse import ArgumentError
from getpass import getpass
from io import TextIOWrapper
from tempfile import NamedTemporaryFile, TemporaryFile
from typing import Callable
from typing import Union

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives.serialization import BestAvailableEncryption, Encoding, load_pem_private_key, load_pem_public_key, load_ssh_private_key, load_ssh_public_key, NoEncryption, \
    PrivateFormat, PublicFormat

from keysec.parser import in_arg


class Key:
    def __init__(self):
        self.orig_str: str = None
        self.key: Union[Ed25519PrivateKey, Ed25519PublicKey, RSAPrivateKey, RSAPublicKey] = None
        self.orig_format: Union[PrivateFormat, PublicFormat] = None
        self.password: str = ''
        self.comment: str = None

    def is_ssh(self) -> bool:
        return self.orig_format is PrivateFormat.OpenSSH or self.orig_format is PublicFormat.OpenSSH

    def is_private(self) -> bool:
        return isinstance(self.orig_format, PrivateFormat)

    def is_public(self) -> bool:
        return isinstance(self.orig_format, PublicFormat)

    def load_key(self, key_str: str):
        if self.key is not None:
            return
        self.orig_str = key_str.strip()
        key_bytes = key_str.encode('utf-8')
        loaded_key, orig_format, password = None, None, ''
        funcs = ((load_pem_private_key, PrivateFormat.PKCS8), (load_ssh_private_key, PrivateFormat.OpenSSH),
                 (load_pem_public_key, PublicFormat.SubjectPublicKeyInfo), (load_ssh_public_key, PublicFormat.OpenSSH))
        for load in funcs:
            try:
                loaded_key, orig_format = load[0](key_bytes, password=None) if isinstance(load[1], PrivateFormat) else load[0](key_bytes), load[1]
                break
            except (ValueError, TypeError) as error:
                if error.args[0] == 'Key is password-protected.' or error.args[0] == 'Password was not given but private key is encrypted':
                    password = getpass('Enter current key passphrase: ')
                    try:
                        loaded_key, orig_format = load[0](key_bytes, password=password.encode('utf-8')), load[1]
                        break
                    except:
                        raise ValueError('Entered passphrase is incorrect.') from None
            except:
                pass
        if loaded_key is None:
            raise ArgumentError(argument=in_arg, message='input is not an OpenSSL or OpenSSH ASCII-encoded key')
        self.key, self.orig_format, self.password = loaded_key, orig_format, password

    def get_ssh_comment(self) -> str:
        if self.comment is not None or not self.is_ssh():
            return self.comment
        public = self.orig_str
        if self.orig_format is PrivateFormat.OpenSSH:
            with NamedTemporaryFile(mode='w+', encoding='utf-8') as tmp:
                write_output(self.orig_str, tmp, close=False)
                public = subprocess.run(['ssh-keygen', '-y', '-P', self.password, '-f', tmp.name], capture_output=True, text=True, check=True).stdout
        with TemporaryFile(mode='w+', encoding='utf-8') as tmp:
            write_output(public, tmp, close=False)
            tmp.seek(0)
            info = subprocess.run(['ssh-keygen', '-l', '-f', '-'], capture_output=True, text=True, check=True, stdin=tmp).stdout
        self.comment = ' '.join(info.split(' ')[2:-1])
        return self.comment

    def to_str(self, str_format: Union[PrivateFormat, PublicFormat] = None, comment: str = None, password: str = None) -> str:
        str_format = str_format if str_format is not None else self.orig_format
        password = password if password is not None else self.password
        encoding = Encoding.OpenSSH if str_format is PublicFormat.OpenSSH else Encoding.PEM

        if isinstance(str_format, PrivateFormat):
            if self.is_public():
                raise ValueError('cannot convert a public key into a private one')
            if password:
                res = self.key.private_bytes(encoding=encoding, format=str_format, encryption_algorithm=BestAvailableEncryption(password.encode('utf-8')))
            else:
                res = self.key.private_bytes(encoding=encoding, format=str_format, encryption_algorithm=NoEncryption())
        else:
            if self.is_private():
                res = self.key.public_key().public_bytes(encoding=encoding, format=str_format)
            else:
                res = self.key.public_bytes(encoding=encoding, format=str_format)
        res = res.decode('utf-8').strip()

        if self.is_ssh() and str_format in (PrivateFormat.OpenSSH, PublicFormat.OpenSSH):
            comment = comment if comment is not None else self.get_ssh_comment()
        if comment and (str_format is PublicFormat.OpenSSH):
            res += f' {comment}'
        elif comment and (str_format is PrivateFormat.OpenSSH):
            with NamedTemporaryFile(mode='w+', encoding='utf-8') as tmp:
                write_output(res, tmp, close=False)
                subprocess.run(['ssh-keygen', '-c', '-C', comment, '-P', password, '-f', tmp.name], capture_output=True, text=True, check=True)
                tmp.seek(0)
                res = tmp.read().strip()
        return res


def write_output(text: str, file: TextIOWrapper, close=True):
    file.write(text + '\n')
    file.flush()
    if close and not file.name == '<stdout>':
        file.close()


def generate_and_write(output: TextIOWrapper, func: Callable[..., str], *args, **kwargs):
    key = func(*args, **kwargs)
    write_output(text=key, file=output)


def full_process(key_str: str, output: TextIOWrapper, func: Callable[[Key, ...], str], *args, **kwargs):
    key = Key()
    key.load_key(key_str=key_str)
    res = func(key, *args, **kwargs)
    write_output(text=res, file=output)
