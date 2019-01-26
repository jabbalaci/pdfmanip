#!/usr/bin/env python3

"""
pdfmanip
--------

Manipulate PDF files (e.g. remove given pages)

https://github.com/jabbalaci/pdfmanip

by Laszlo Szathmary (jabba.laci@gmail.com)
"""

import os
import readline
import sys
from collections import deque
from typing import Deque, List

import pikepdf
from pikepdf import Pdf
from pyrsistent import freeze, pvector, v
from pyrsistent.typing import PVector

VERSION = "0.1"
OUTPUT = 'output.pdf'
VIEWER = "okular"


def usage() -> None:
    text = f"""
PDF Manipulator v{VERSION} by Laszlo Szathmary (jabba.laci@gmail.com), 2019
Usage:

pdfmanip input.pdf

Then the program switches to interactive mode.
""".strip()
    print(text)


def print_help() -> None:
    text = f"""
h, help        - this help
q, quit        - quit
i, info        - info about the status of the output.pdf
w              - write output.pdf (fails if the file exists)
w!             - overwrite output.pdf
d, ls          - directory list
oi             - open input.pdf with {VIEWER}
oo             - open output.pdf with {VIEWER}
del PAGES      - delete the given pages
                 the format of PAGES is like printing pages
                 example: del 1,2-4,8-
reload, reset  - reload input.pdf
                 useful if you deleted some wrong pages and you want to restart
""".strip()
    print(text)


def get_pages(s: str, last: int) -> PVector[int]:
    s = s.strip()
    if len(s) == 0:
        return v()

    li: List[int] = []
    #
    for piece in s.split(','):
        pos = piece.find('-')
        if pos > -1:
            n1 = int(piece[:pos])
            if piece.endswith('-'):
                n2 = last
            else:
                n2 = int(piece[pos+1:])
            li.extend(range(n1, n2+1))
        else:
            li.append(int(piece))
    #
    return freeze(li)


def print_info(pdf: Pdf) -> None:
    print("Number of pages: {}".format(len(pdf.pages)))


def write_file(pdf: Pdf, overwrite=False) -> None:
    if os.path.isfile(OUTPUT):
        if not overwrite:
            print("Warning! The file output.pdf already exists")
            return
        #
    #
    pdf.save(OUTPUT)
    os.system(f"ls -al | grep {OUTPUT}")


def open_pdf(fname: str, what: str) -> None:
    if what == "input":
        os.system(f"{VIEWER} {fname} &>/dev/null &")
    if what == "output":
        if os.path.isfile(OUTPUT):
            os.system(f"{VIEWER} {OUTPUT} &>/dev/null &")
        else:
            print(f"Warning: {OUTPUT} doesn't exist")


def delete_pages(pdf: Pdf, pages: PVector[int]) -> Pdf:

    def minus_one(q: Deque[int]) -> Deque[int]:
        res: Deque[int] = deque([])
        for n in q:
            res.append(n - 1)
        return res

    q = deque(pages)
    q = minus_one(q)
    while len(q) > 0:
        del pdf.pages[q.popleft()]
        q = minus_one(q)
    #
    return pdf


def process(fname: str) -> None:
    if not os.path.isfile(fname):
        print("Error: the input file doesn't exist", file=sys.stderr)
        exit(1)
    # else
    print("type 'h' for help")

    pdf = pikepdf.open(fname)
    print_info(pdf)

    while True:
        try:
            inp = input("> ").strip()
        except (KeyboardInterrupt, EOFError):
            print()
            print("bye")
            exit()
        #
        if inp == "":
            continue
        elif inp in ('h', 'help'):
            print_help()
        elif inp in ('q', 'quit'):
            print("bye")
            break
        elif inp in ('i', 'info'):
            print_info(pdf)
        elif inp == 'w':
            write_file(pdf, overwrite=False)
        elif inp == 'w!':
            write_file(pdf, overwrite=True)
        elif inp in ('d', 'ls'):
            os.system("ls -al")
        elif inp == 'oi':
            open_pdf(fname, what="input")
        elif inp == 'oo':
            open_pdf(fname, what="output")
        elif inp == "del":
            print("provide the pages too")
        elif inp.startswith("del "):
            text = "".join(inp.split(" ")[1:])
            pages = get_pages(text, len(pdf.pages))
            # print(pages)
            pdf = delete_pages(pdf, pages)
            print_info(pdf)
            print("# nothing was saved yet")
        elif inp in ("reload", "reset"):
            pdf = pikepdf.open(fname)
            print_info(pdf)
        else:
            print("What?")

##############################################################################

if __name__ == "__main__":
    if len(sys.argv) == 1:
        usage()
        exit(1)
    # else
    process(sys.argv[1])
