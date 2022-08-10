#!/usr/bin/env python3
# encoding:utf-8

# More on how to configure this file here: https://setuptools.readthedocs.io/en/latest/setuptools.html#metadata
from autopackage.parsers.setup_parser import SetupParser
from setuptools import find_packages

name = 'keysec'

version = '1.1.1'

description = 'With this program you will be able to generate OpenSSL and OpenSSH keys (RSA, Ed25519) and carry out transformations between both formats.'

with open("README.md", "r") as fh:
    long_description = fh.read()

author = 'Fernando Enzo Guarini'
author_email = 'fernandoenzo@gmail.com'

url = 'https://github.com/fernandoenzo/keysec'
download_url = 'https://github.com/fernandoenzo/keysec'

packages = find_packages()

licencia = 'GPLv3+'

zip_safe = False

keywords = 'openssl openssh key private public rsa ed25519 elliptic curve cyrptography convert transform keys format pem pkcs'

python_requires = '>=3.9'

install_requires = [
    'cryptography >= 37.0.4',
]

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: End Users/Desktop',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Topic :: Security',
    'Topic :: Security :: Cryptography',
    'Topic :: Communications',
    'Topic :: Internet',
    'Topic :: System :: Networking',
    'Topic :: Utilities',
]

entry_points = {
    'console_scripts': [
        'keysec = keysec.keysec:main',
    ]
}

package_data = {
    'keysec': [
        'libs/*.whl',
    ],
}

SetupParser(name=name, version=version, packages=packages, description=description, long_description=long_description, long_description_content_type="text/markdown", author=author,
            author_email=author_email, url=url, download_url=download_url, install_requires=install_requires, license=licencia, python_requires=python_requires, keywords=keywords,
            classifiers=classifiers, entry_points=entry_points, package_data=package_data, zip_safe=zip_safe)
