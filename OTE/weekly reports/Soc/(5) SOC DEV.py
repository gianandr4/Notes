#!/usr/bin/env python3

import datetime
import win32com.client
import time
from statistics import median,stdev,mean
import statistics as st
import pandas as pd

def calc(x):
    x=time.strftime('%H:%M:%S', time.gmtime(x))
    return(x)

def COM(b):
    b=b.replace('\r\n','')
    start='SR: '
    end='Παρακαλώ για τις ενέργειες σας'
    try:
        b=b.split(start)[1].split(end)[0]
        b=[b[:13],b[14:]]
        if b[1]=='':b[1]=obj.subject
        return b
    except:
        b=b.split()
        for line in b:
            if len(line) == 13 and line[:2]=='1-':
                return([line,obj.subject])
        return['N/A',obj.subject]


def DSLAM(s,b=None):
    s=(s.replace("_", " "))
    s=s.split()
    for line in s:
        if line.isdigit() and len(line)>3 and len(line)<6:
            return(line)    
#    b=b.replace('_',' ')
#    b=b.split()
#    for line in b:
#        if line.isdigit() and len(line)>3 and len(line)<6:
#            return(line)
    return'NA'
    
    
###############################################################################
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)
messages = inbox.Items#-----------------------------------------------INIT
messages.Sort("[ReceivedTime]", True)
message = messages.GetLast()#-----------------------------------------INIT
# TOTAL NUMBER OF EMAILS IN THE FOLDER
print("Total number",len(inbox.items))
start_time = time.time()
#MENUMENUMENUMENUMENUMENUMENUMENUMENUMENUMENUMENUMENUMENUMENUMENUMENUMENUMENU
print("SOC \n----\n")
input("To date(dd/mm/yyyy): ")
messages = messages.Restrict("[ReceivedTime] >= '" +frodate.format(datetime,'%m/%d/%Y %H:%M %p')+"'")
input("To date(dd/mm/yyyy): ")
messages = messages.Restrict("[ReceivedTime] <= '" +todate.format(datetime,'%m/%d/%Y %H:%M %p')+"'")
print("Total messages: ",len(messages),'from: ',frodate,'to',todate,'\n\n')


objects=[]
c=0
c1=0
c2=0
c3=0
counter=0
l=[]
e=[]
msg=[]
for message in messages:
    msg.append(message)

for message in msg:
    try:
        if 'soc' in str(message.sender):
#            print(message.sender)+
            objects.append(message)
#            print(message.sender,'___',message.subject,'__',message.receivedtime)
            l.append([str(message.sender),str(message.receivedtime),str(message.subject)])
        subj=message.subject
        if 'soc_tele' in str( message.sender):
#            print('Tel :',c1,message.receivedtime,message.subject)
            c1+=1     
        elif 'soc_internet_tv' in str(message.sender):
#            print('Net :',c2,message.receivedtime,message.subject)
            c2+=1
        elif 'soc-rfr' in str(message.sender):
#            print('Rfr :',c3,message.receivedtime,message.subject)
            c3+=1
    except:
        if message.subject.startswith('Rural North Πιθανό Πρόβλημα Dslam IMATH_FITIA_D_ALC_90409 κάρτα 1'):
            print(message.subject)
        counter+=1
#        print('lost:',counter)
        e.append(message)
errors=[]
test=[]      
#print('Tele: ',c1,'\nNet: ',c2,'\nRfr: ',c3)
dfx=[]
for obj in objects:
    if obj.subject.startswith('RE:'):continue
    mr=obj.receivedtime
    ms=obj.subject
    mc=COM(obj.body)
    try:
        if 'MSAN'.upper() in obj.subject.upper():
            print('MSAN----------',DSLAM(ms),mc)
            dfx.append(([DSLAM(ms)]+['MSAN']+[str(mr)]+mc))
        elif 'κάρτα'.upper() in obj.subject.upper():
            print('CARD----------',DSLAM(ms),mc)
            dfx.append(([DSLAM(ms)]+['CARD']+[str(mr)]+mc))
        elif 'dslam offline'.upper() in obj.subject.upper(): 
            print('OFF-----------',DSLAM(ms),mc)
            dfx.append(([DSLAM(ms)]+['OFF']+[str(mr)]+mc))
        elif obj.subject.upper().startswith('Πιθανό Πρόβλημα Dslam'.upper()):
            print('UNRE----------',DSLAM(ms),mc)
            dfx.append(([DSLAM(ms)]+['UNREGISTERED']+[str(mr)]+mc))
            #unregistered catcher
        else:
            print('ERROR',obj.subject,mc)
            test.append(obj)
    except:
        errors.append(obj)
for error in errors:
    print(obj.subject)
    
#df=pd.DataFrame(l)
#print(df.to_string())

dfxx=pd.DataFrame(dfx)
dfxx.columns=['Code','Type','SR','Received on','Comment']
dfxx.to_excel(excel_writer=input('Type file name: ')+'.xlsx',engine='xlsxwriter')

#print(dfxx.to_string())


'''
dslam offline FTIO_KENOURIO_D_HUA 28576 
Πιθανό Πρόβλημα Dslam MESSI_ANO.DORIO_D_HUA_16273_KV
Πιθανό Πρόβλημα Dslam MESSI_AGIA.KYRIAKI_D_HUA_12799 κάρτα 5
Πιθανό Πρόβλημα MSAN στο  Dslam KEFAL_MESOVOUNIA_D_HUA_28339_KV
Rural North Πιθανό Πρόβλημα Dslam IMATH_FITIA_D_ALC_90409 κάρτα 1
'''

