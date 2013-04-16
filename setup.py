#!/usr/bin/env python
#-*- coding:utf8 -*-
import os
from setuptools import setup, find_packages

setup(  name='bless',
        author = 'loveguoguo',
        packages = find_packages(),
        install_requires = ['django>=1.4.2', 'mmseg', ],
        dependency_links = [
            'https://pypi.python.org/pypi/mmseg/1_3_0',
        ],
    )
