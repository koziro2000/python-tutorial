# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 11:57:43 2018

@author: jroh
"""

import csv

tagLogFile = open("EodFiles.tlg", "r")
for line in tagLogFile:
    fields = line.split(";")
    
    print(fields)
    
tagLogFile.close()


