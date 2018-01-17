# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

install_requires = [
    'beautifulsoup4',
    'lxml',
    'requests',
    'stackshare',
    'sqlalchemy',
    'PyMySQL',
    'redis',
    'aiohttp',
    'async_timeout'
]

setup(
    name='stackshare',
    version='0.0.1',
    license='MIT',
    author='zengtong',
    author_email='unixsudo@outlook.com',
    description='stackshare info download',
    # package_dir={'': 'stackshare'},
    install_requires=install_requires
)
