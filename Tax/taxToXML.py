# -*- coding: utf-8 -*-

import pandas as pd
import contextlib, os
import numpy as np

strInputXlsFile = "T1204.xlsx"
strInputWS = "2017 T1204 Values"

dtT1204 = pd.ExcelFile(strInputXlsFile);
dtT1204 = dtT1204.parse(strInputWS);

#Remove unnecessary rows
x1 = dtT1204;
x1 = x1.drop(x1.index[[1, 2, 3, 4, 5]])

#Rename columns with first record
x1.columns = x1.iloc[0]
x1 = x1.iloc[1:]

xmlBeginning = '<?xml version="1.0" encoding="UTF-8"?> '+\
'\n<Submission xmlns:ccms="http://www.cra-arc.gc.ca/xmlns/ccms/1-0-0" ' +\
 ' xmlns:sdt="http://www.cra-arc.gc.ca/xmlns/sdt/2-2-0" ' +\
 ' xmlns:ols="http://www.cra-arc.gc.ca/enov/ol/interfaces/efile/partnership/ols/1-0-1" ' +\
 ' xmlns:ols1="http://www.cra-arc.gc.ca/enov/ol/interfaces/efile/partnership/ols1/1-0-1"' +\
 ' xmlns:ols10="http://www.cra-arc.gc.ca/enov/ol/interfaces/efile/partnership/ols10/1-0-1"' +\
 ' xmlns:ols100="http://www.cra-arc.gc.ca/enov/ol/interfaces/efile/partnership/ols100/1-0-1"' +\
 ' xmlns:ols12="http://www.cra-arc.gc.ca/enov/ol/interfaces/efile/partnership/ols12/1-0-1"' +\
 ' xmlns:ols125="http://www.cra-arc.gc.ca/enov/ol/interfaces/efile/partnership/ols125/1-0-1"' +\
 ' xmlns:ols140="http://www.cra-arc.gc.ca/enov/ol/interfaces/efile/partnership/ols140/1-0-1"' +\
 ' xmlns:ols141="http://www.cra-arc.gc.ca/enov/ol/interfaces/efile/partnership/ols141/1-0-1"' +\
 ' xmlns:ols2="http://www.cra-arc.gc.ca/enov/ol/interfaces/efile/partnership/ols2/1-0-1"' +\
 ' xmlns:ols5="http://www.cra-arc.gc.ca/enov/ol/interfaces/efile/partnership/ols5/1-0-1"' +\
 ' xmlns:ols50="http://www.cra-arc.gc.ca/enov/ol/interfaces/efile/partnership/ols50/1-0-1"' +\
 ' xmlns:ols52="http://www.cra-arc.gc.ca/enov/ol/interfaces/efile/partnership/ols52/1-0-1"' +\
 ' xmlns:ols6="http://www.cra-arc.gc.ca/enov/ol/interfaces/efile/partnership/ols6/1-0-1"' +\
 ' xmlns:ols8="http://www.cra-arc.gc.ca/enov/ol/interfaces/efile/partnership/ols8/1-0-1"' +\
 ' xmlns:ols8-1="http://www.cra-arc.gc.ca/enov/ol/interfaces/efile/partnership/ols8-1/1-0-1"' +\
 ' xmlns:ols9="http://www.cra-arc.gc.ca/enov/ol/interfaces/efile/partnership/ols9/1-0-1"' +\
 ' xmlns:olsbr="http://www.cra-arc.gc.ca/enov/ol/interfaces/efile/partnership/olsbr/1-0-1"' +\
 ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' +\
 ' xsi:noNamespaceSchemaLocation="layout-topologie.xsd">'



#T619 node
def T619(row):
    xml = ['<T619>']
    xml.append('<sbmt_ref_id>{0}</sbmt_ref_id>'.format('000T1204'))
    xml.append('<rpt_tcd>{0}</rpt_tcd>'.format('O'))
    xml.append('<trnmtr_nbr>{0}</trnmtr_nbr>'.format('MM555555'))
    xml.append('<trnmtr_tcd>{0}</trnmtr_tcd>'.format('1'))
    xml.append('<summ_cnt>{0}</summ_cnt>'.format('000001'))
    xml.append('<lang_cd>{0}</lang_cd>'.format('E'))

    xml.append('<TRNMTR_NM>')
    xml.append('<l1_nm>{0}</l1_nm>'.format('Canada Pension Plan'))
    xml.append('<l2_nm>{0}</l2_nm>'.format('Investment Board'))
    xml.append('</TRNMTR_NM>')

    xml.append('<TRNMTR_ADDR>')
    xml.append('<addr_l1_txt>{0}</addr_l1_txt>'.format('ONE QUEEN STREET EAST'))
    xml.append('<addr_l2_txt>{0}</addr_l2_txt>'.format('Suite 2500'))
    xml.append('<cty_nm>{0}</cty_nm>'.format('Toronto'))
    xml.append('<prov_cd>{0}</prov_cd>'.format('ON'))
    xml.append('<cntry_cd>{0}</cntry_cd>'.format('CAN'))
    xml.append('<pstl_cd>{0}</pstl_cd>'.format('M5C2W5'))
    xml.append('</TRNMTR_ADDR>')

    xml.append('<CNTC>')
    xml.append('<cntc_nm>{0}</cntc_nm>'.format('Cindy S. Lee'))
    xml.append('<cntc_area_cd>{0}</cntc_area_cd>'.format('416'))
    xml.append('<cntc_phn_nbr>{0}</cntc_phn_nbr>'.format('479-5531'))
    #xml.append('<cntc_extn_nbr>{0}</cntc_extn_nbr>'.format(''))
    xml.append('<cntc_email_area>{0}</cntc_email_area>'.format('cindy.lee@cppib.com'))
    #xml.append('<sec_cntc_email_area>{0}</sec_cntc_email_area>'.format('cindy.lee@cppib.com'))
    xml.append('</CNTC>')
    
    xml.append('</T619>')
    return '\n'.join(xml)


def appendXML(xml, tag, value):
    tagString = '<'+tag+'><![CDATA[{0}]]></'+tag+'>';
    if (pd.notnull(value)):
        xml.append(tagString.format(value))
    return xml

#T1204 Slip Generator
def T1204Slip(row):
    xml = ['<T1204Slip>']
    
    if(pd.notnull(row['Sole proprietorship recipient last name ']) or 
       pd.notnull(row['Sole proprietorship recipient first name ']) or
       pd.notnull(row['Sole proprietorship recipient first name '])):
        xml.append('<RCPNT_NUM>')
        appendXML(xml, 'snm', row['Sole proprietorship recipient last name '])    
        appendXML(xml, 'gvn_nm', row['Sole proprietorship recipient first name '])    
        appendXML(xml, 'init', row['Sole proprietorship recipient initial '])
        xml.append('</RCPNT_NUM>')

    appendXML(xml, 'sin', row['Recipient social insurance number (SIN) '])    
    appendXML(xml, 'rcpnt_bn', row['Recipient Account Number '])
    
    xml.append('<RCPNT_BUS_NM>')
    appendXML(xml, 'l1_nm', row['Recipient business name - line 1 '])
    appendXML(xml, 'l2_nm', row['Recipient business name - line 2 '])
    xml.append('</RCPNT_BUS_NM>')
    
    appendXML(xml, 'rcpnt_tcd', row['Recipient type code '])
   
    xml.append('<RCPNT_BUS_ADDR>')
    appendXML(xml, 'addr_l1_txt', row['Recipient business address - line 1 '])
    appendXML(xml, 'addr_l2_txt', row['Recipient business address - line 2 '])
    appendXML(xml, 'cty_nm', row['Recipient city '])
    appendXML(xml, 'prov_cd', row['Recipient province or territory code '])
    appendXML(xml, 'cntry_cd', row['Recipient country code '])
    appendXML(xml, 'pstl_cd', row['Recipient postal code '])
    xml.append('</RCPNT_BUS_ADDR>')

    appendXML(xml, 'payr_bn',row['Payer Business Number (BN) '])

    xml.append('<T1204_AMT>')

    appendXML(xml, 'srvc_pay_amt',row['Service payments only '])
    appendXML(xml, 'mxd_gd_pay_amt',row['Mixed services and goods payments '])

    xml.append('</T1204_AMT>')

    appendXML(xml, 'ptnrp_filr_id',row['Partnership filer identification number (FIN) '])
    appendXML(xml, 'rpt_tcd',row[18])


    xml.append('</T1204Slip>')
    
    return '\n'.join(xml)

def T1204Summary(row):
    xml = ['\n<T1204Summary>']
    appendXML(xml, 'bn',row['Business Number (BN) '])

    xml.append('<PAYR_NM>')
    appendXML(xml, 'l1_nm',row['Payer name - line 1 '])
    appendXML(xml, 'l2_nm',row['Payer name - line 2 '])
    appendXML(xml, 'l3_nm',row['Payer name - line 3 '])
    xml.append('</PAYR_NM>')

    xml.append('<PAYR_ADDR>')
    appendXML(xml, 'addr_l1_txt', row['Payer address - line 1 '])
    appendXML(xml, 'addr_l2_txt', row['Payer address - line 2 '])
    appendXML(xml, 'cty_nm', row['Payer city '])
    appendXML(xml, 'prov_cd', row['Payer province or territory code '])
    appendXML(xml, 'cntry_cd', row['Payer country code '])
    appendXML(xml, 'pstl_cd', row['Payer postal code '])
    xml.append('</PAYR_ADDR>')

    xml.append('<CNTC>')
    appendXML(xml, 'cntc_nm', row['Contact name '])
    appendXML(xml, 'cntc_area_cd', row['Contact area code '])
    appendXML(xml, 'cntc_phn_nbr', row['Contact telephone number'])
    appendXML(xml, 'cntc_extn_nbr', row['Contact extension '])
    xml.append('</CNTC>')

    appendXML(xml, 'tx_yr', row['Taxation year '])
    appendXML(xml, 'slp_cnt', row['Total number of T1204 slip records '])
    appendXML(xml, 'rpt_tcd', row['Report Type Code '])
    appendXML(xml, 'fileramendmentnote', row['Filer amendment note\xa0 '])

    xml.append('<T1204_TAMT>')
    appendXML(xml, 'tot_srvc_pay_amt', row['Total service payments '])
    appendXML(xml, 'tot_mxd_gd_pay_amt', row['Total mixed services and goods payments '])

    xml.append('</T1204_TAMT>')

    xml.append('</T1204Summary>')

    return '\n'.join(xml)

allColumns = x1.columns.values

x1Summary = x1.iloc[0:1, 19:]
xmlSummary = '\n'.join(x1Summary.apply(T1204Summary, axis=1))
xml619 = T619(1)
xml1 = '\n'.join(x1.apply(T1204Slip, axis=1))
#xml1 = xmlBeginning + '\n<Submission>\n' + xml619 + '\n<Return>\n<T1204>\n' + xml1 + xmlSummary + '\n</T1204>\n</Return>\n</Submission>' 

xml1 = xmlBeginning + '\n' + xml619 + '\n<Return>\n<T1204>\n' + xml1 + xmlSummary + '\n</T1204>\n</Return>\n</Submission>' 

filename = 'sampleT1024.xml';
with contextlib.suppress(FileNotFoundError):
    os.remove(filename)

with open(filename, 'a') as the_file:
    the_file.write(xml1)
