#!/usr/bin/env python

import sys
import os
from distutils.core import setup

import ftl

setup(name='for-the-loot',
      version=ftl.__version__,
      description='Hack and slay dungeon crawler.',
      long_description=ftl.__doc__,
      #author=ftl.__author__,
      #author_email=ftl.__email__,
      #url='',
      packages=['ftl'],
      license='MIT',
      platforms = 'any',
      classifiers=['Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
      ],
     )



