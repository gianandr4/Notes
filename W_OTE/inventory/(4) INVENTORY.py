#!/usr/bin/env python
#create a dataframe for the according DSLAM

import datetime
import pandas as pd
import win32com.client
import time

def CARD(b):
    start='Τύπος κάρτας'.upper()
    end='S/N'
    try:
        b=b.upper().split(start)[1].split(end)[0]
        b=b.replace(':','')
        b=b.replace('/','')
        b=b.replace(' ','')
        b=b.replace('\t','')
        b=b.replace('\r\n','')
        return (b)
    except:
        start='Τύπος Κάρτας'.upper()
        end='S/N '
    b=b.replace('\r\n','')
    try:
        b=b.split(start)[1].split(end)[0]
        b=b.replace(':','')
        b=b.replace(' ','')
        b=b.replace('\t','')

        return (b)
    except:
        start='Τύπος καρτας'
        end='S/N '
    try:
        b=b.split(start)[1].split(end)[0]
        b=b.replace(':','')
        b=b.replace(' ','')
        b=b.replace('\t','')

        return (b)
    except:
        start='Τύποι καρτών'
        end='S/N '
    try: 
        b=b.split(start)[1].split(end)[0]
        b=b.replace(':','')
        b=b.replace(' ','')
        b=b.replace('\t','')
        return (b)
    except:
        if 'NDLT-G' in obj.subject:
            return('NDLT-G')
        else:
            return ('N/A')

    
def DSLAM(s,b):
    s=(s.replace("_", " "))
    s=s.split()
    for line in s:
        if line.isdigit() and len(line)>3 and len(line)<6:
            return(line)    
    b=b.replace('_','#')
    b=b.split('#')
    for line in b:
        if line[0:5].isdigit():
            return(line[0:5])
        elif line[0:4].isdigit():
            return(line[0:4])
    return''
    


ALL_CARDS=['NDLT-G', 'NDLT-J', 'NVLT-P', 'NTLT', 'NDPS', 'ADLE',
           'ADPD', 'VCMM', 'ADEF', 'VDSH', 'ADB', 'ASDA', 'NANT','NALT-J',
           'NDLT-J', 'VPEC', 'ASRB', 'ASPB', 'SDMM','UP2A ','NPOT-C',
           'NVLT-P', 'SCUN', 'VCM', 'NPOT-C', 'CCUC' ]

###############################################################################
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6).Folders.Item("INVENTORY")
messages = inbox.Items#-----------------------------------------------INIT
messages.Sort("[ReceivedTime]", True)
message = messages.GetLast()#-----------------------------------------INIT
# TOTAL NUMBER OF EMAILS IN THE FOLDER
start_time = time.time()  


frodate='1/1/2020'#input("From date(dd/mm/yyyy): ")
messages = messages.Restrict("[ReceivedTime] > '" +frodate.format(datetime,'%m/%d/%Y')+"'")
todate='17/1/2020'#input("To date(dd/mm/yyyy): ")
messages = messages.Restrict("[ReceivedTime] < '" +todate.format(datetime,'%m/%d/%Y')+"'")# %H:%M %p

print("Total messages: ",len(messages))

limit=0
Texn=[]
date=''
objects=[]
for message in messages:
    for recipient in message.Recipients:
        if message.subject.startswith('RE'):continue
        if message.subject.startswith('Απ:'):continue


        if not 'ΤΕΧΝΙΚΗ ΥΠΟΣΤΗΡΙΞΗ' in message.subject:continue
        if not 'DL-GRC01-Τμήμα Λειτουργίας Δικτύου Μετάδοσης' in str(recipient):continue 
        
#        if 'Santovnitsis'.upper() in message.body.upper():
#            print ('nai')
#            continue
            
        date,sep,tail=str(message.receivedtime).partition(' ')
        Texn.append([date,str(message.subject)])
        objects.append(message)
    previous=message.receivedtime      
print(time.time()-start_time)


pd.options.display.max_colwidth = 100
df=pd.DataFrame(Texn)
#print('\n',df.to_string())
error=[]
temp=''
dslam=[]
card=0
fant=0
subr=0
a=0
b=0
c=0
xxx=[0,10,11,12,18,19,20,21,22,23,24,28]
cc=0
slot=0
'''
2019-11-14 15:17:39+00:00 - anorthotiko

'''
for k,obj in enumerate (objects):
    hualc=''
    karta=''
    temp=DSLAM(obj.subject,obj.body)
    
    m=obj.body.upper()
    if '_HUA_' in m:
        hualc='Huawei'
    elif '_ALU_' in m or '_ALC_' in m:
        hualc='Alcatel'
#    m=m.replace(' ','')
#    m=m.replace('\r\n\r\n','#')
#    m=m.replace('/','')
#    x=m.split('#')
#    if 'Santovnitsis'.upper() in m:
#        dslam.append(['SAVRO','','','','','','1'])
#        print(k)
#        continue
    
    for cardd in ALL_CARDS:
        if cardd in obj.body:
            xxx=True
#            karta=CARD(m)
            if not cardd in karta:
                karta+=cardd+' '
                card+=1

    
    if xxx:
        dslam.append([temp,card,0,0,0,hualc,karta])
        xxx=False
        card=0
    
#    else:
#         dslam.append([temp,1,0,0,0,hualc,''])
#    karta=''
#    error.append(obj)
#
#    continue

    
            
        
    #        print('\n----',i,obj.subject,'----\n')
    
    if ' FAN' in obj.body.upper() or 'FAN TRAY' in obj.body.upper() or 'FAN TRAY' in obj.subject.upper():
        fant+=1
#        print('fan')
        dslam.append([temp,0,1,0,0,0,'notacard'])
#        print('FAN TRAY FAN TRAY \nFAN TRAY FAN TRAY ',m)
    elif 'SUBRACK' in m or 'SUBRACK' in m:
        subr+=1
#        print('sub')
        dslam.append([temp,0,0,1,0,0,0])
#        print('SUBRACK SUBRACK\nSUBRACK SUBRACK',m)
    elif 'RMU' in m or 'POWER MONITORING UNIT' in m:
        a+=1
#        print('rmu')
        dslam.append([temp,0,0,0,1,0,0])

    elif 'SWITCH' in m or 'SWITCHES' in m:
        b+=1
#        print('switch')
        dslam.append([temp,0,0,0,0,1,0])
    elif message.subject.startswith('RE'):
        dslam.append(['RERERE','','','','','','1'])

#        continue       

#    else:
    error.append(obj)
#        input('NEXT')
    
        

        
        
df1=pd.DataFrame(dslam)
df1.columns=['Code','Card','Fan','Subrack','Rmu','Switch','card']
df2=df1.sort_values(by=['card','Fan','Subrack','Rmu','Switch',],ascending=False).reset_index(drop=True)
 
#df1 = df1[df1.duplicated(['Code'])]        
#print('Total: ',i,'\nCards: ',card,'\nFan tray: ',fant,'\nSubracks:',subr,'\nRMU: ',a)
        


df1.to_excel(excel_writer=input('Type file name: ')+'.xlsx',engine='xlsxwriter')


