#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Setup MyMoney Investment."""

import os
import pathlib
from setuptools import setup, find_packages

HERE = pathlib.Path(__file__).parent

README = (HERE / 'README.md').read_text()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup_options = dict(
    name='mymoney',
    version='0.1',
    author='Ravi Boodher',
    maintainer='Navi Tech',
    maintainer_email='raviboodher@gmail.com',
    author_email='raviboodher@gmail.com',
    url='https://www.navi.com/en-id/',
    description=f'Money APP - Investment Portfolio Tracker!',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['tests*']),
    package_data={'': ['*']},
    include_package_data=True,
    install_requires=required,
    extras_require={},
    entry_points={
        'console_scripts': [
            'mymoney=mymoney.geektrust:main',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'Environment :: Console',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Operating System :: Unix',
    ],
    python_requires='>=3.6',
)

setup(**setup_options)
