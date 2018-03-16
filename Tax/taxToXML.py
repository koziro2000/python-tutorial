# -*- coding: utf-8 -*-

import pandas as pd
import contextlib, os

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
    xml.append('<cntc_extn_nbr>{0}</cntc_extn_nbr>'.format(''))
    xml.append('<cntc_email_area>{0}</cntc_email_area>'.format('cindy.lee@cppib.com'))
    xml.append('<sec_cntc_email_area>{0}</sec_cntc_email_area>'.format('cindy.lee@cppib.com'))
    xml.append('</CNTC>')
    
    xml.append('</T619>')
    return '\n'.join(xml)


def T1204Slip(row):
    xml = ['<T1204Slip>']
    xml.append('<RCPNT_NUM>')
    xml.append('<snm>{0}</snm>'.format(row['Sole proprietorship recipient last name ']))
    xml.append('<gvn_nm>{0}</gvn_nm>'.format(row['Sole proprietorship recipient first name ']))
    xml.append('<init>{0}</init>'.format(row['Sole proprietorship recipient initial ']))
    xml.append('</RCPNT_NUM>')
    xml.append('<sin>{0}</sin>'.format(row['Recipient social insurance number (SIN) ']))
    xml.append('<rcpnt_bn>{0}</rcpnt_bn>'.format(row['Recipient Account Number ']))
    
    xml.append('<RCPNT_BUS_NM>')
    xml.append('<l1_nm>{0}</l1_nm>'.format(row['Recipient business name - line 1 ']))
    xml.append('<l2_nm>{0}</l2_nm>'.format(row['Recipient business name - line 2 ']))
    xml.append('</RCPNT_BUS_NM>')
    
    xml.append('<rcpnt_tcd>{0}</rcpnt_tcd>'.format(row['Recipient type code ']))
   
    xml.append('<RCPNT_BUS_ADDR>')
    xml.append('<addr_l1_txt>{0}</addr_l1_txt>'.format(row['Recipient business address - line 1 ']))
    xml.append('<addr_l2_txt>{0}</addr_l2_txt>'.format(row['Recipient business address - line 2 ']))
    xml.append('<cty_nm>{0}</cty_nm>'.format(row['Recipient city ']))
    xml.append('<prov_cd>{0}</prov_cd>'.format(row['Recipient province or territory code ']))
    xml.append('<cntry_cd>{0}</cntry_cd>'.format(row['Recipient country code ']))
    xml.append('<pstl_cd>{0}</pstl_cd>'.format(row['Recipient postal code ']))
    xml.append('</RCPNT_BUS_ADDR>')

    xml.append('<payr_bn>{0}</payr_bn>'.format(row['Payer Business Number (BN) ']))

    xml.append('<T1204_AMT>')

    xml.append('<srvc_pay_amt>{0}</srvc_pay_amt>'.format(row['Service payments only ']))
    xml.append('<mxd_gd_pay_amt>{0}</mxd_gd_pay_amt>'.format(row['Mixed services and goods payments ']))

    xml.append('</T1204_AMT>')

    xml.append('<ptnrp_filr_id>{0}</ptnrp_filr_id>'.format(row['Partnership filer identification number (FIN) ']))
    xml.append('<rpt_tcd>{0}</rpt_tcd>'.format(row[18]))


    xml.append('</T1204Slip>')
    
    return '\n'.join(xml)

def T1204Summary(row):
    xml = ['<T1204Slip>']
    xml.append('<T1204Summary>')
    xml.append('<bn>{0}</bn>'.format(row['Business Number (BN) ']))

    xml.append('<PAYR_NM>')
    xml.append('<l1_nm>{0}</l1_nm>'.format(row['Payer name - line 1 ']))
    xml.append('< l2_nm>{0}</l2_nm>'.format(row['Payer name - line 2 ']))
    xml.append('<l3_nm>{0}</l3_nm>'.format(row['Payer name - line 3 ']))
    xml.append('</PAYR_NM>')

    xml.append('<PAYR_ADDR>')
    xml.append('<addr_l1_txt>{0}</addr_l1_txt>'.format(row['Payer address - line 1 ']))
    xml.append('<addr_l2_txt>{0}</addr_l2_txt>'.format(row['Payer address - line 2 ']))
    xml.append('<cty_nm>{0}</cty_nm>'.format(row['Payer city ']))
    xml.append('< prov_cd>{0}</prov_cd>'.format(row['Payer province or territory code ']))
    xml.append('<cntry_cd>{0}</cntry_cd>'.format(row['Payer country code ']))
    xml.append('<pstl_cd>{0}</pstl_cd>'.format(row['Payer postal code ']))
    xml.append('</PAYR_ADDR>')

    xml.append('<CNTC>')
    xml.append('<cntc_nm>{0}</cntc_nm>'.format(row['Contact name ']))
    xml.append('< cntc_area_cd>{0}</cntc_area_cd>'.format(row['Contact area code ']))
    xml.append('<cntc_phn_nbr>{0}</cntc_phn_nbr>'.format(row['Contact telephone number']))
    xml.append('< cntc_extn_nbr>{0}</cntc_extn_nbr>'.format(row['Contact extension ']))
    xml.append('</CNTC>')

    xml.append('< tx_yr>{0}</tx_yr>'.format(row['Taxation year ']))
    xml.append('<slp_cnt>{0}</slp_cnt>'.format(row['Total number of T1204 slip records ']))
    xml.append('< rpt_tcd>{0}</rpt_tcd>'.format(row['Report Type Code ']))
    xml.append('<fileramendmentnote></fileramendmentnote>'.format(row['Filer amendment note\xa0 ']))

    xml.append('<T1204_TAMT>')
    xml.append('<tot_srvc_pay_amt>{0}</tot_srvc_pay_amt>'.format(row['Total service payments ']))
    xml.append('<tot_mxd_gd_pay_amt>{0}</tot_mxd_gd_pay_amt>'.format(row['Total mixed services and goods payments ']))

    xml.append('</T1204_TAMT>')

    xml.append('</T1204Summary>')

    return '\n'.join(xml)

allColumns = x1.columns.values

x1Summary = x1.iloc[0:1, 19:]
xmlSummary = '\n'.join(x1Summary.apply(T1204Summary, axis=1))
xml619 = T619(1)
xml1 = '\n'.join(x1.apply(T1204Slip, axis=1))
xml1 = '<Submission>\n' + xml619 + '\n<Return>\n<T1204>\n' + xml1 + xmlSummary + '\n<\T1204>\n</Return>\n</Submission>' 

filename = 'sampleT1024.xml';
with contextlib.suppress(FileNotFoundError):
    os.remove(filename)

with open(filename, 'a') as the_file:
    the_file.write(xml1)

###


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