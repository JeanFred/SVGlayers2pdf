SVGlayers2pdf
=============

Converting SVG Inkscape layers to PDF


Usage
-----

`svglayers2pdf my_SVG_file`

Use `svglayers2pdf --help` for help on using the conversion script.


Installation
------------

Easiest way to install is to use `pip`:

    `pip install -e git://github.com/JeanFred/SVGlayers2pdf.git#egg=SVGLayers2pdf`

Alternatively, you can clone the repository and install it using `setuptools`:
    `python setup.py install`

This will install in `/usr/local/bin/` the executable entry-point `svglayers2pdf`


Dependencies
------------

SVGlayers2pdf makes use of:
- argparse (built-in with Python 2.7)
- lxml, to parse the SVG XML tree
- pyPdf, to join the individual PDFs into one
- Inkscape, using system calls, to generate PDF from SVG

All Python dependencies should be resolved at installation time.
