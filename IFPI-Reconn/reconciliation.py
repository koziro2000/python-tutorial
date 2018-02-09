# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 18:04:59 2017

@author: jroh
"""

import pandas as pd
import numpy as np

scd_cash_file = 'PIRE_149_Daily_Cash_Reconciliation.csv'
tick_trans_file = 'PIRE-149_PI_Ticketing_Tickets.csv'
cusip_mapping_file = 'Investran-CUSIP_SCDID_Mapping.xlsx'

SCD_Data = pd.read_csv(scd_cash_file)
Ticketing_Data = pd.read_csv(tick_trans_file, encoding = "ISO-8859-1")
cusip_mapping = pd.read_excel(cusip_mapping_file, sheetname="cusip_lookup", index_col = "CUSIP", squeeze=True)

SCD_Data['SCD_Trx_No'] = SCD_Data['Transaction No. In Originating']
Ticketing_Data['Ticket_No'] = Ticketing_Data['Ticket']

SCD_Data = SCD_Data.set_index(['Transaction No. In Originating'])
Ticketing_Data = Ticketing_Data.set_index(['Ticket'])

#complete_reconn = pd.merge(SCD_Data, on = 'index' Ticketing_Data, how = 'outer')
recon_only_matching = Ticketing_Data.join(SCD_Data, how='left', rsuffix = '_SCD')
recon_only_matching = recon_only_matching.iloc[2:]
recon_only_matching ['diff'] = recon_only_matching['Net Proceeds QC'].astype(float).fillna(0.0) - recon_only_matching['Investment Amount'].astype(float).fillna(0.0)
SCD_Data_join_recon = recon_only_matching[['SCD_Trx_No', 'Ticket_No', 
                                           'diff', 'Net Proceeds QC', 'Investment Amount', 
                                           'Due_Settlement_Date', 'Settlement Date',
                                           'Trade Date','Trade Date_SCD',
                                           'Funding Currency','Settlement Currency Code - Transaction',
                                           'SCDID_CUSIP','Security ID - Current',
                                           'Model Portfolio','Model Portfolio Code']]

SCD_Data_join_recon['Due_Settlement_Date'] = pd.to_datetime(SCD_Data_join_recon['Due_Settlement_Date'], format='%Y-%m-%d %H:%M:%S.%f', errors='ignore')
SCD_Data_join_recon['Settlement Date'] = pd.to_datetime(SCD_Data_join_recon['Settlement Date'], format='%Y%m%d', errors='ignore')
SCD_Data_join_recon['Trade Date_SCD'] = pd.to_datetime(SCD_Data_join_recon['Trade Date_SCD'], format='%Y%m%d', errors='ignore')
SCD_Data_join_recon['Trade Date'] = pd.to_datetime(SCD_Data_join_recon['Trade Date'], format='%Y%m%d  %H:%M:%S.%f', errors='ignore')


#Insert columns for matching results with default values
#Better to re-arrange columns after matchings done
SCD_Data_join_recon.insert(loc=7, column='SDT_Diff', value=False)
SCD_Data_join_recon.insert(loc=10, column='TDT_Diff', value=False)
SCD_Data_join_recon.insert(loc=13, column='CURR_Diff', value=False)
SCD_Data_join_recon.insert(loc=16, column='SCDID_Diff', value=False)
SCD_Data_join_recon['MP_Diff'] = False

SCD_Data_join_recon['SDT_Diff'] = np.where((SCD_Data_join_recon['Due_Settlement_Date'] != SCD_Data_join_recon['Settlement Date']), True, False)
SCD_Data_join_recon['TDT_Diff'] = np.where((SCD_Data_join_recon['Trade Date'] != SCD_Data_join_recon['Trade Date_SCD']), True, False)
SCD_Data_join_recon['CURR_Diff'] = np.where((SCD_Data_join_recon['Funding Currency'] != SCD_Data_join_recon['Settlement Currency Code - Transaction']), True, False)
SCD_Data_join_recon['SCDID_Diff'] = np.where((SCD_Data_join_recon['SCDID_CUSIP'] != SCD_Data_join_recon['Security ID - Current']), True, False)
SCD_Data_join_recon['MP_Diff'] = np.where((SCD_Data_join_recon['Model Portfolio'] != SCD_Data_join_recon['Model Portfolio Code']), True, False)

SCD_Data_join_recon['NEW_CUSIP'] = SCD_Data_join_recon['SCDID_CUSIP']

# new cusip dictionary
cusip_mapping = cusip_mapping.to_dict()

SCD_Data_join_recon['NEW_CUSIP'] = SCD_Data_join_recon['NEW_CUSIP'].map(cusip_mapping)

# introduce new logic to match "New Cusip" to the "SCDID_CUSIP"
SCD_Data_join_recon['NEW_CUSIP_Diff'] = np.where((SCD_Data_join_recon['NEW_CUSIP'] != SCD_Data_join_recon['Security ID - Current']), True, False)



writer = pd.ExcelWriter('SCD_Data_join.xlsx', engine='xlsxwriter')
SCD_Data_join_recon.to_excel(writer, sheet_name='Sheet1')
worksheet = writer.sheets['Sheet1']
writer.save()

notMatchingTickets = SCD_Data_join_recon[
        (SCD_Data_join_recon['diff'] != 0) | 
        (SCD_Data_join_recon['SDT_Diff'] == True)  | 
        (SCD_Data_join_recon['TDT_Diff'] == True)  | 
        (SCD_Data_join_recon['CURR_Diff'] == True) | 
        (SCD_Data_join_recon['SCDID_Diff'] == True) | 
        (SCD_Data_join_recon['MP_Diff'] == True)  | 
        (SCD_Data_join_recon['NEW_CUSIP_Diff'] == True) ]


writer = pd.ExcelWriter('SCD_Data_notMatching.xlsx', engine='xlsxwriter')
SCD_Data_join_recon.to_excel(writer, sheet_name='Sheet1')
worksheet = writer.sheets['Sheet1']
writer.save()

