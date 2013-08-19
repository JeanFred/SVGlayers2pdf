#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import svglayers2pdf
    version = svglayers2pdf.__version__
except ImportError:
    version = 'Undefined'

packages = ['svglayers2pdf']
requires = ['pyPdf', 'lxml', 'argparse']
scripts  = []

setup(
      name='SVGlayers2pdf',
      version      = version,
      author       = 'Jean-Frédéric, Alexandre Bourget',
      url          = 'http://github.com.org/JeanFred/SVGlayers2pdf',
      description  = 'Converting SVG Inkscape layers to PDF',
      license      = 'GPLv3',
      entry_points = {
        'console_scripts': [
            'layers2pdf = svglayers2pdf.SVGconvert:main',
            ]
        },
      packages=packages,
      requires=requires,
      scripts=scripts,
)
