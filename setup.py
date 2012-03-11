# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os
import telecaster

CLASSIFIERS = ['Environment :: Web Environment', 'Framework :: Django', 'Intended Audience :: Science/Research', 'Intended Audience :: Education', 'Programming Language :: Python', 'Programming Language :: JavaScript', 'Topic :: Internet :: WWW/HTTP :: Dynamic Content', 'Topic :: Internet :: WWW/HTTP :: WSGI :: Application', 'Topic :: Multimedia :: Sound/Audio', 'Topic :: Multimedia :: Sound/Audio :: Analysis', 'Topic :: Multimedia :: Sound/Audio :: Players', 'Topic :: Scientific/Engineering :: Information Analysis', 'Topic :: System :: Archiving',  ]

setup(
  name = "TeleCaster",
  url = "http://parisson.com",
  description = "open web audio CMS",
  long_description = open('README.rst').read(),
  author = "Guillaume Pellerin",
  author_email = "yomguy@parisson.com",
  version = telecaster.__version__,
  install_requires = [
        'django>=1.3.1',
        'django-json-rpc',
        'deefuzzer',
        'south',
  ],
  platforms=['OS Independent'],
  license='CeCILL v2',
  classifiers = CLASSIFIERS,
  packages = find_packages(),
  include_package_data = True,
  zip_safe = False,
)