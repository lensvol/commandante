# -*- coding: utf-8 -*-

import os
from setuptools import setup, Command


DESCRIPTION = 'Find and fix missing trailing commas in Python collections.'


def get_version():
    with open('commandante/__init__.py') as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='commandante',
    version=get_version(),
    author='Kirill Borisov',
    author_email='lensvol@gmail.com',
    description=DESCRIPTION,
    license='MIT',
    keywords='commandante',
    url='https://github.com/lensvol/commandante',
    packages=['commandante'],
    long_description=DESCRIPTION,
    install_requires=[
        'click>=4.1',
        'redbaron>=0.5.1',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Operating System :: POSIX',
    ],
    entry_points={
        'console_scripts': [
            'commandante = commandante.main:processor',
        ],
    },
)
