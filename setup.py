#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2011-2018, Yelp, Inc.
import os

from setuptools import setup

setup(
    name='gdg-pisa-user-manager',
    version='1.0.0',
    license='MIT License',
    description='Bot for managing the Telegram group of GDG Pisa',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    author='GDG Pise',
    author_email='TODO',
    url='https://github.com/gdgpisa/gdgpisausermanager/',
    py_modules=['gdgpisausermanager'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Communications :: Chat',
        'Topic :: Internet',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=['python-telegram-bot'],
    entry_points={'console_scripts': ['gdg-pisa-user-manager = gdgpisausermanager:main']},
)
