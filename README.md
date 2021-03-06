pdfmanip
========

A simple tool to manipulate your PDF files.

Motivation
----------

I prefer reading on paper, so I print a lot. Often, when
I export for instance a blog post in PDF, there are
some pages that I don't want to print.

This little tool helps me removing the unwanted pages easily.

Demo
----

You must provide the input PDF and then it goes to interactive mode.
The output is written to `output.pdf`.

```
$ ./pdfmanip.py input.pdf
type 'h' for help
Number of pages: 8
> h
h, help        - this help
q, quit        - quit
i, info        - info about the status of the output.pdf
w              - write output.pdf (fails if the file exists)
w!             - overwrite output.pdf
d, ls          - directory list
oi             - open input.pdf with okular
oo             - open output.pdf with okular
del PAGES      - delete the given pages
                 the format of PAGES is like printing pages
                 example: del 1,2-4,8-
reload, reset  - reload input.pdf
                 useful if you deleted some wrong pages and you want to restart
> del 1,6-
Number of pages: 4
# nothing was saved yet
> w!
-rw-r--r--   1 jabba users 110024 Jan  6 15:15 output.pdf
>
```

Here, the input PDF had 8 pages. After removing pages 1, 6, 7 and 8, we
got a PDF with 4 remaining pages.

Dependency
----------

The real PDF manipulation is done with the [pikepdf](https://github.com/pikepdf/pikepdf)
library.

Supported platform
------------------

Linux only.

Reddit discussion
-----------------

See [here](https://old.reddit.com/r/Python/comments/ad617g/a_cli_util_to_manipulate_pdf_files_eg_remove/).

Related work
------------

* [pikepdf](https://github.com/pikepdf/pikepdf) Python library (this is what I used)
* [pdftk](https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/), a powerful PDF-manipulating command-line tool
* [PDFsam](https://pdfsam.org/) ([wikipedia article](https://en.wikipedia.org/wiki/PDF_Split_and_Merge)), a more heavyweight solution for manipulating your PDFs
