# -*- coding: utf-8 -*-

import pandas as pd
import contextlib, os

from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
from xml.etree import ElementTree

dtT1204 = pd.ExcelFile("T1204.xlsx");
dtT1204.sheet_names
dtT1204 = dtT1204.parse("2017 T1204 Values");

x1 = dtT1204;
x1 = x1.drop(x1.index[[1, 2, 3, 4, 5]])

#Rename collumns
x1.columns = x1.iloc[0]
x1 = x1.iloc[1:]

x1.head()

def func(row):
    xml = ['<item>']
    for field in row.index:
        xml.append(' <field name="{0}">{1}</field>'.format(field, row[field]))
    xml.append('</item>')
    return '\n'.join(xml)


def T1204Slip(row):
    xml = ['<T1204Slip>']
    xml.append('<RCPNT_NUM>')
    xml.append('<snm>{0}</snm>'.format(row[0]))
    xml.append('<gvn_nm>{0}</gvn_nm>'.format(row[1]))
    xml.append('<init>{0}</init>'.format(row[2]))
    xml.append('</RCPNT_NUM>')
    xml.append('<sin>{0}</sin>'.format(row[3]))
    xml.append('<rcpnt_bn>{0}</rcpnt_bn>'.format(row['Recipient Account Number ']))
    xml.append('</T1204Slip>')
    
    return '\n'.join(xml)


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def T1204SlipGenXML(row):
    top = Element('T1204Slip')
    child = SubElement(top, 'RCPNT_NUM')
    child = SubElement(child, 'snm')
    child.text = row[0]
    
    print(prettify(top))    

xml1 = '\n'.join(x1.apply(T1204SlipGenXML, axis=1))
xml1 = '<Return>\n' + xml1 + '</Return>'



filename = 'sampleT1024.xml';

with contextlib.suppress(FileNotFoundError):
    os.remove(filename)

with open(filename, 'a') as the_file:
    the_file.write(xml1)

###
'Sole proprietorship recipient last name ',
'Sole proprietorship recipient first name ',
'Sole proprietorship recipient initial ',

'Recipient social insurance number (SIN) ', 
'Recipient Account Number ',

'Recipient business name - line 1 ',
'Recipient business name - line 2 ', 
'Recipient type code ',

'Recipient business address - line 1 ',
'Recipient business address - line 2 ', 
'Recipient city ',
'Recipient province or territory code ', 
'Recipient country code ',
'Recipient postal code ', 

'Payer Business Number (BN) ',

'Service payments only ', 
'Mixed services and goods payments ',

'Partnership filer identification number (FIN) ', 
'Report Type Code ',


# Summary

'Business Number (BN) ', 

'Payer name - line 1 ', 
'Payer name - line 2 ',
'Payer name - line 3 ', 

'Payer address - line 1 ',
'Payer address - line 2 ', 
'Payer city ',
'Payer province or territory code ', 
'Payer country code ',
'Payer postal code ', 

'Contact name ', 
'Contact area code ',
'Contact telephone number', 
'Contact extension ', 

'Taxation year ',
'Total number of T1204 slip records ', 
'Report Type Code ',

'Filer amendment note  ', 
'Total service payments ',
'Total mixed services and goods payments '
###