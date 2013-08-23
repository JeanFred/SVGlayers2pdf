# -=- encoding: utf-8 -=-

"""Converts SVG layers to PDF."""


# Original code :
# Author: Alexandre Bourget
# Copyright (c) 2008: Alexandre Bourget
# LICENSE: GPLv3
#Simplified from https://github.com/abourget/inkscapeslide/blob/master/inkscapeslide/__init__.py :
#Edit by Jean-Frédéric

import lxml.etree
import os
from os.path import abspath, join
import subprocess

import tempfile
from shutil import rmtree
import logging
import argparse


class SVGconvert():

    """Converting a SVG file to PDF."""

    def __init__(self, filehandler=None):
        """Constructor."""
        self.filepath = filehandler.name
        self.svg = filehandler.read()
        self.tempdir = tempfile.mkdtemp()

    def _get_filename(self):
        """Return the filename from the filepath."""
        return os.path.basename(self.filepath)

    def _get_dirname(self):
        """Return the directory of the SVG file."""
        return os.path.dirname(self.filepath)

    def _clean_up(self):
        """Clean up by removing the temporary directory."""
        rmtree(self.tempdir)

    def convert_SVG_to_PDF(self):
        """Convert the SVG to PDF."""
        pdfslides = self._convert_SVG_layers_to_PDF()
        self._merge_PDFs(pdfslides)
        self._clean_up()

    def _convert_SVG_layers_to_PDF(self):
        """Convert all SVG layers to PDFs files.

        Return the list of PDFs.

        """
        svgbis = self.svg.replace("style=\"display:none\"",
                                  "style=\"display:inline\"")
        svgbisfile = join(self.tempdir, "file.svg")
        with open(svgbisfile, 'w') as f2:
            f2.write(svgbis)
        logging.info("Using %s as temporary directory", self.tempdir)
        doc = lxml.etree.fromstring(svgbis)
        pdfslides = []
        layers = [x for x in doc.iterdescendants(tag='{http://www.w3.org/2000/svg}g')
                  if x.attrib.get('{http://www.inkscape.org/namespaces/inkscape}groupmode', False) == 'layer']
        for i, layer in enumerate(layers):
            pdfslide = abspath(join(self.tempdir,
                                    "%s.p%d.pdf" % (self._get_filename(), i)))
            label = layer.attrib.get('{http://www.inkscape.org/namespaces/inkscape}label')
            layer_id = layer.attrib.get('id')
            logging.info("Converting %s...", label)
            cmd = "inkscape -A=%s "\
                  "--export-area-page "\
                  "--export-id=%s %s" % (pdfslide, layer_id, svgbisfile)
            logging.debug(cmd)
            subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE,
                             cwd=self._get_dirname()).communicate()
            pdfslides.append(pdfslide)
        return pdfslides

    def _merge_PDFs(self, pdfslides):
        """Merge the given PDFs into one."""
        output_filename = "%s.pdf" % self._get_filename().split(".svg")[0]
        output_filepath = abspath(join(os.curdir, output_filename))
        has_pyPdf = False
        try:
            import pyPdf
            has_pyPdf = True
        except ImportError:
            pass

        if has_pyPdf:
            logging.info("Using 'pyPdf' to join PDFs to %s", output_filepath)
            output = pyPdf.PdfFileWriter()
            inputfiles = []
            for slide in pdfslides:
                inputstream = file(slide, "rb")
                inputfiles.append(inputstream)
                reader = pyPdf.PdfFileReader(inputstream)
                output.addPage(reader.getPage(0))
            outputStream = file(output_filepath, "wb")
            output.write(outputStream)
            outputStream.close()
            for f in inputfiles:
                f.close()
        else:
            logging.warning("PyPDF not installed, cannot merge PDF slides")


def main():
    """Main method, entry point of the script."""
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("svgfilepath", type=argparse.FileType('r'),
                        metavar="SVG file",
                        help='The SVG file to convert')

    parser.add_argument("-v", "--verbose",
                        action="store_true",
                        dest="verbose",
                        default=False,
                        help="Displays INFO messages")
    args = parser.parse_args()

    if args.verbose:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING
    logging.basicConfig(level=log_level)
    logging.info("Starting")

    if args.svgfilepath:
        SVGconvert(args.svgfilepath).convert_SVG_to_PDF()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
