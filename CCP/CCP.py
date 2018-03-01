# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 11:57:43 2018

@author: jroh
"""

import csv


#Loop through each line and parse each string into Dictionary ... to access each code
#How to organize this to show to user? Would Tree Structure Works?

fullCodes = {}
d = {}
lis = []
tagLogFile = open("EodFiles.tlg", "r")
for line in tagLogFile:
    fields = line.split(";")
    
    print(fields)
    d = {}
    for item in fields:
        l = item.split('=')
        d[l[0]] = l[1]
        fullCodes[l[0]] = l[1]
    lis.append(d)
tagLogFile.close()
print(d)


for line in lis:
    print(line['5679'])

import PyPDF2
pdfFileObj = open('CDCC_PDF.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pdfReader.numPages

pageObj = pdfReader.getPage(14)
pageObj.extractText().split('\n')


w = csv.writer(open("FullCodes.csv", "w"))
for key, val in fullCodes.items():
    w.writerow([key, val])




from tkinter import *
import ttk

root = Tk()

tree = ttk.Treeview(root)

tree["columns"]=("one","two")
tree.column("one", width=100 )
tree.column("two", width=100)
tree.heading("one", text="coulmn A")
tree.heading("two", text="column B")

tree.insert("" , 0,    text="Line 1", values=("1A","1b"))

id2 = tree.insert("", 1, "dir2", text="Dir 2")
tree.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A","2B"))

##alternatively:
tree.insert("", 3, "dir3", text="Dir 3")
tree.insert("dir3", 3, text=" sub dir 3",values=("3A"," 3B"))

tree.pack()
root.mainloop()
