import csv
import glob
import os
from datetime import datetime,time
import pandas as pd
import re

                   
list_of_files = glob.glob('C:/Users/kpapaioa.TMNA/Downloads/*.csv') # * means all if need specific format then *.csv
latest_csv = max(list_of_files, key=os.path.getctime)


df=pd.read_csv(latest_csv,'r',delimiter='\t',encoding="UTF-16")
df=df[['SR Number','Priority','Owner Group','Fault Synopsis','SR Comments']]

def create(og):
    df1=pd.DataFrame({'SR Number':['----------'],'Priority':['----------'],'Owner Group':['----------'],'Fault Synopsis':['----------'],'SR Comments':['----------']})
    df2=df.loc[(df['Priority'] == 'CRITICAL' ) & (df['Owner Group']==og)]
    df2.loc[:,'Priority'] = '[fade][color=#FF0000][b]' + df2['Priority'] + '[/b][/color][/fade]'
    df3=df.loc[(df['Priority'] == 'MAJOR') & (df['Owner Group']==og)]
    df3.loc[:,'Priority']= '[fade][color=#FF0000][b]' + df3['Priority'] + '[/b][/color][/fade]'

    df_all=(df1.append(df2,sort=False).append(df3,sort=False)).reset_index(drop=True)
    df_all['Priority']= '' + df_all['Priority'] + ''
    
    
    for i,text in enumerate(df_all['SR Comments']):
        text=str(text)
        if text.startswith('----'):continue
        if text.startswith('Dslam_code'):
            print('ada')
            text='__Dslam Code: ' + ', '.join(re.findall(r'Dslam_code: (\d{4}\d?) EETT:',text))
        if ('Τα παρακάτω dslam έχουν επανέλθει:' in text) or ('Τα παρακάτω dslam είναι ακόμα κάτω:' in text):
            text1='Τα παρακάτω dslam έχουν επανέλθει: ' + ', '.join(re.findall(r'dslam: (\d{4}\d?) επανήλθε',text)) +'\n'
            text2='Τα παρακάτω dslam είναι ακόμα κάτω: '+ ', '.join(re.findall(r'dslam: (\d{4}\d?) έπεσε',text)) +'\n'
            text=text1+text2
        df_all.at[i,'SR Comments']=text    
            
    return df_all# (df_all.to_csv(sep='|',index=False,line_terminator='|\r\n'))

def snowflake():
    with open("skata.txt","w+",encoding='utf-16') as f:
        f.write('[b]ΑΝΑΦΟΡΑ ΠΑΡΑΔΟΣΗΣ ΒΑΡΔΙΑΣ[/b]\n')
        f.write('\n[b]NCC-PATRA-DATA/IP[/b]\n')
        f.write(patr.to_csv(sep='|',index=False,line_terminator='|\n'))
        f.write('\n[b]NCC-THESS-DATA/IP[/b]\n')
        f.write(thess.to_csv(sep='|',index=False,line_terminator='|\n'))
        f.write('\n[b]NCC-CRETE-DATA/IP[/b]\n')
        f.write(crete.to_csv(sep='|',index=False,line_terminator='|\n'))
    

def common(text):
    with open("skata.txt","w+",encoding='utf-16') as f:    
        ctt=input('Enter Ctt count: ')
        f.write('[b]ΑΝΑΦΟΡΑ '+ text + ' ΒΑΡΔΙΑΣ[/b]\n')
        f.write('\nNTT Count|CTT Count|\n')
        f.write('|----------|----------|\n')
        f.write('|'+str(len(df))+'|'+ctt +'|\n')
        f.write('\n[b]NMC-DATA/IP[/b]\n')
        f.write(ath.to_csv(sep='|',index=False,line_terminator='|\n'))
        f.write('\n[highlight=yellow][b]RURAL[/b][/highlight]\n')
        

_1_ = ['08','09']
_2_ = ['14','15']
_3_ = ['22','23']
_4_ = ['06','07']

ath=create('NMC-DATA/IP')
patr=create('NCC-PATRA-DATA/IP')
thess=create('NCC-THESS-DATA/IP')
crete=create('NCC-CRETE-DATA/IP')

inputs=["1","2","3","4","exit","EXIT","?"]
case=None
auto=datetime.today().strftime('%H')
end=False

while True:
    manual=''
    if not auto in _1_+_2_+_3_+_4_:  
        print(
'''            ____________________________________         
           | COULD NOT DETECT AUTOMATICALLY!!!  |
           |____________________________________|''')
        while manual not in inputs:
            manual=input(
'''            ____________________________________         
           |   REPORTER MENU: Input(1,2,3,4):   |
           |____________________________________|
           | ANAFORA PARADOSHS VARDIAS:     (1) |
           | ANAFORA PRWINHS VARDIAS:       (2) |
           | ΑNAFORA APOGEYMATINHS VARDIAS: (3) |
           | ΑNAFORA VRADINIS VARDIAS:      (4) |
           | Info:                          (?) |
           | Exit:                     ('exit') |
           -------------------------------------- 
           >>> ''')
            if manual not in inputs:
                print("\n\nWRONG INPUT!")    

    
    if auto in _1_ or manual=='1':
        snowflake()
        break
    elif auto in _2_ or manual=='2':
        common('ΠΡΩΙΝΗΣ')
        break
    elif auto in _3_ or manual=='3':
        common('ΑΠΟΓΕΥΜΑΤΙΝΗΣ')
        break
    elif auto in _4_ or manual=='4':
        common('ΝΥΚΤΕΡΙΝΗΣ')
        break      
    
    elif manual=='?':
        print('''
              Detects time and chooses the right report to create.\n
              If the time is between 8:00 and 9:59 -> Anafora paradoshs
              If the time is between 6:00 and 7:59 -> Prwinh anafora
              If the time is between 14:00 and 15:59 -> Apogeymatinh anafora
              If the time is between 22:00 and 23:59 -> Nykterinh anafora
              ''')
        input('\nContinue..')
    elif manual.upper() == 'EXIT':
        break
    
        








    



#if case != 'exit':
os.startfile('skata.txt')
##
##





#print("\nFile saved as: "+name)
#
##if input("Open notepad (Y/N): ") in ["Y","y"]:    
#os.startfile(name)
#
##if input("Open Csv (Y/N): ") in ["Y","y"]:
#if not input("TYPE Y TO OPEN CSV OR ENTER TO CLOSE: ") != "Y":
#    os.startfile(latest_csv)
















