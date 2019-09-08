#Setup script for ABvalidator
from __future__ import print_function
from setuptools import setup,find_packages
import codecs
import os
import sys
import re

HERE = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    #Return multiple read calls to different readable objects as a single string.
   
    return codecs.open(os.path.join(HERE, *parts), 'r', encoding='utf-8').read()

LONG_DESCRIPTION = read('README.md')


setup(
    name='ABvalidator',
    version='0.0.1',
    url='https://github.com/ernstmul/abvalidator/',
    license='Apache Software License',
    author='Ernst Mulders',
    install_requires=[
        'PyInquirer>=1.0.3',
        'colorama>=0.4.1',
        'prompt_toolkit==1.0.14',
        'Pygments>=2.2.0',
        'regex>=2016.11.21',
        'scipy>=1.3.1',
        'pandas>=0.25.1',
        'statsmodels>=0.10.1',
        'numpy>=1.17.2',
        'scikit-learn>=0.21.3'
        ],
    author_email='ernst@mulde.rs',
    description='A/B experiment and platform validation toolkit',
    long_description=LONG_DESCRIPTION,    
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    package_data={'ABvalidator': ['data/*.json']},
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering'
        ],
)