import PyPDF2
pdfFileObj = open('samplePdf.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

page = pdfReader.getPage(0)

page_content = page.extractText()

print(page_content)

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import HTMLConverter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
from io import BytesIO
import re
import csv


def convert_pdf_to_html(path):
    rsrcmgr = PDFResourceManager()
    #retstr = StringIO()
    retstr = BytesIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = HTMLConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open('samplePdf.pdf', 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0 #is for all
    caching = True
    pagenos=set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str


endResultHtml = convert_pdf_to_html(path = 'samplePdf.pdf')

with open("Output.html", "w") as text_file:
    print("{}".format(endResultHtml), file=text_file)