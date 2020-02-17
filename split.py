from PyPDF2 import PdfFileWriter, PdfFileReader
from copy import copy
from os import path
import argparse

title_margin = 150
tb_margin = 50
lr_margin = 40
inner_margin = 8
safety_margin = 4
suffix = "(Cropped)"

parser = argparse.ArgumentParser()
parser.add_argument("filename")
args = parser.parse_args()

filename = args.filename
base_name = path.splitext(filename)[0]

if base_name.endswith(suffix):
    exit(0)

with open(filename, "rb") as in_f:
    input1 = PdfFileReader(in_f)
    output = PdfFileWriter()

    numPages = input1.getNumPages()
    print("document has %s pages." % numPages)

    for i in range(numPages):
        page = input1.getPage(i)
        w = page.mediaBox.getUpperRight_x()
        h = page.mediaBox.getUpperRight_y()

        x0 = lr_margin
        x1 = w / 2 - inner_margin / 2
        x2 = w / 2 + inner_margin / 2
        x3 = w - lr_margin

        y0 = tb_margin
        y1 = h / 2 + safety_margin
        y2 = h / 2 - safety_margin
        y3_ = h - tb_margin
        y3 = y3_ - title_margin if i == 0 else y3_

        def add_page(ll, ur):
            page_ = copy(page)
            page_.cropBox.lowerLeft = ll
            page_.cropBox.upperRight = ur
            output.addPage(page_)

        add_page((x0, y2), (x1, y3))
        add_page((x0, y0), (x1, y1))
        add_page((x2, y2), (x3, y3))
        add_page((x2, y0), (x3, y1))

    with open(f"{base_name} {suffix}.pdf", "wb") as out_f:
        output.write(out_f)