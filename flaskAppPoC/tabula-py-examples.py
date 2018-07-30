import tabula
import pandas

firstFileName = "firstExample.pdf";
secondFileName = "secondExample.pdf";


firstDf = tabula.read_pdf(firstFileName, output_format='dataframe', multiple_tables = True, encoding='cp1252', pages="9")
secondDf = tabula.read_pdf(secondFileName, output_format='dataframe',  multiple_tables = True, encoding='cp1252', pages="46-47")

writer = pandas.ExcelWriter('CVCExtract.xlsx', engine='xlsxwriter')
firstDf[0].to_excel(writer, sheet_name='First')
secondDf[0].to_excel(writer, sheet_name='Second')
writer.save()


ohJson = firstDf[0].to_json(orient='split')


import PyPDF2
pdfFileObj = open("firstExample.pdf", 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

page = pdfReader.getPage(8)

page_content = page.extractText()

print(page_content)

