#!/usr/bin/env python

__author__ = 'Shaun Rong'
__version__ = '0.1'
__maintainer__ = 'Shaun Rong'
__email__ = 'rongzq08@gmail.com'

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(name='MultiFil',
          version=__version__,
          description="Filter out promising diffusive cathode structures for MV batteries",
          author="Ziqin (Shaun) Rong",
          author_email="rongzq08@mit.edu",
          license="MIT License",
          packages=find_packages(),
          zip_safe=False,
          install_requires=["pymatgen", "fireworks"],
          classifiers=["Development Status :: 2 - Pre-Alpha", "rogramming Language :: Python :: 2.7",
                       "Topic :: Scientific/Engineering :: Physics"])