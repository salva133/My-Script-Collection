"""
Script Name: HTML2PDF.py
Description: This script converts an HTML file into a PDF document using the WeasyPrint library. It is designed to be a simple and direct way to create a PDF version of a static HTML page.

Usage:
    - The script is currently set to convert 'index.html' to 'ausgabe.pdf'.
    - To convert a different HTML file, replace 'index.html' with the path to the desired file.
    - The output PDF will be named 'ausgabe.pdf', but this can be changed to any desired output file name.
"""


from weasyprint import HTML

HTML("index.html").write_pdf("ausgabe.pdf")
