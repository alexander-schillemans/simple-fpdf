# Simple FPDF
A simplified version of the FPDF package.

## Aim of this package
This package aims to make it easier to generate a PDF, without concerning yourself with the difficulties of keeping track of the (x,y) position inside the document.

A simple row-column system is used to generate a PDF and insert text.
Since this extends the FPDF package, all the FPDF functionalities are still included.

# Getting started

### Install

Install with pip.

```python
pip install simple-fpdf
```

### Import

Import the package and SimpleFPDF.

```python
from simple_fpdf import SimpleFPDF
```

# How to use

## Initialize SimpleFPDF

SimpleFPDF is initialized the same as a normal FPDF. You can also use the `width` and `height` parameters. If no `format`, `width` or `height` is specified, A4 will be used.

```python
pdf = SimpleFPDF(orientation='P', unit='mm', format="A4")
pdf = SimpleFPDF(orientation='P', unit='mm', width=210, height=297)
```

## Defining the rows and columns

SimpleFPDF makes use of a simple row-column system where all the rows on the page have an equal height.
Before adding a page, you need to define how many rows a page will have, and how many columns these rows will contain.

```python
page_1_rows = [
    { 'columns' : 1 }, # row 1, has one column
    { 'columns' : 1 }, # row 2, has one column
    { 'columns' : 2 }, # row 3, has two columns
    { 'columns' : 3 } # row 4, has three columns
]
```

## Adding a page

Add a page using the known `.add_page()` method. This method expects a new parameter: `rows`.
Rows need to be an array with the row definitions as specified above.

```python
pdf.add_page(rows=page_1_rows)
```

## Writing text

Once you have a page and their rows and columns, you can simply start writing text to it using `.write_text()`. This function takes three required parameters: `row`, `column` and `txt`.
Optionally, you can also specify the `page` by giving its number. If no page is given, the current page is used.

```python
pdf.write_text(txt='This is my heading', row=1)
pdf.write_text(txt='This is my second row', row=2)
pdf.write_text(txt='This is my thirth row, first column', row=3, column=1)
pdf.write_text(txt='This is my thirth row, second column', row=3, column=2)
pdf.write_text(txt='This is my fourth row, first column', row=4, column=1)
pdf.write_text(txt='This is my fourth row, second column', row=4, column=2)
pdf.write_text(txt='This is my fourth row, thirth column', row=4, column=3)
```

## Output

Generate the pdf using the `.output()` method.

```python
pdf.output('my_pdf.pdf')
```

## Advanced settings

Since SimpleFPDF aims to be as simple as possible, not much customisation is possible.
There are a few settings you can use.

### top-margin

You can specify the `top-margin` for a row. This will add a margin to the top of a row, using the unit specified at creation.

```python
rows = [
    { 'columns' : 1, 'top-margin' : 30 }, # row 1, has one column and a top-margin of 30mm
    { 'columns' : 1 }, # row 2, has one column
    { 'columns' : 2, 'top-margin' }, # row 3, has two columns and a top-margin of 15mm
    { 'columns' : 3 } # row 4, has three columns
]
```