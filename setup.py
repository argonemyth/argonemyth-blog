#!/usr/bin/env python
from setuptools import setup, find_packages

try:
    README = open('README.rd').read()
except:
    README = None

try:
    REQUIREMENTS = open('requirements.txt').read()
except:
    REQUIREMENTS = None

setup(
    name = 'argonemyth-blog',
    version = "0.0.1",
    description = 'A blog engine that use Django REST Framework.',
    long_description = README,
    install_requires = REQUIREMENTS,
    author = 'Fei Tan',
    author_email = 'fei@argonemyth.com',
    url = 'https://github.com/argonemyth/argonemyth-blog',
    packages = find_packages(),
    include_package_data = True,
    classifiers = ['Development Status :: 2 - Pre-Alpha', 
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
    test_suite='tests.main',
)
