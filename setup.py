# -*- coding: utf-8 -*-
setup(
      name='layers2pdf',
      version      = '1.0',
      author       = 'Jean-Frédéric, Alexandre Bourget',
      url          = 'http://github.com.org/JeanFred/layers2pdf',
      description  = 'Converting Inkscape layers SVG to PDF'
      license      = 'GPLv3',
      entry_points = {
        'console_scripts': [
            'layers2pdf = layers2pdf:main',
            ]
        },
      install_requires= ['pyPdf', 'lxml']
)
