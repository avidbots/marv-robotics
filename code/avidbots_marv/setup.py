# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

from setuptools import setup

setup(name='avidbots_marv',
      version='1.0',
      description='Avidbots Marv Code',
      url='',
      author='Avidbots',
      packages=['avidbots_marv'],
      install_requires=['marv',
                        'marv-robotics'],
      include_package_data=True,
      zip_safe=False)
