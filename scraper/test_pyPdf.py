# -*- coding: utf-8 -*-

import pyPdf

from pyPdf import PdfFileReader

import urllib2
import tempfile

response = urllib2.urlopen('http://cbr.ru/credit/depend/RB2574.pdf')
data = response.read()
tmpF = tempfile.NamedTemporaryFile()
tmpF.write(data)
print tmpF.name

pdf = pyPdf.PdfFileReader(tmpF)

content = u""
for i in range(0, pdf.getNumPages()):
    # Extract text from page and add to content
    content += pdf.getPage(i).extractText() + "\n"
    # Collapse whitespace
    # content = " ".join(content.replace("\xa0", " ").strip().split())

print content
# Scheiße!!!!!  Np cyrillic!!!