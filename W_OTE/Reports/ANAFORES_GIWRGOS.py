import csv   #default csv reader
import glob          #to find latest csv
import os         #gia ta windows
import re
from datetime import datetime




def by_owner(owner_group,data,ntt,ctt=None):
    critical=[]
    major=[]
    for row in data:
        if not row[2]==owner_group:continue
        ## text processing for comments
        text = row[4]
        if text.startswith('----'):continue
        if text.startswith('Dslam_code'):
            text='__Dslam Code: ' + ', '.join(re.findall(r'Dslam_code: (\d{4}\d?) EETT:',text))
        if ('Τα παρακάτω dslam έχουν επανέλθει:' in text) or ('Τα παρακάτω dslam είναι ακόμα κάτω:' in text):
            text1='Τα παρακάτω dslam έχουν επανέλθει: ' + ', '.join(re.findall(r'dslam: (\d{4}\d?) επανήλθε',text)) +'\n'
            text2='Τα παρακάτω dslam είναι ακόμα κάτω: '+ ', '.join(re.findall(r'dslam: (\d{4}\d?) έπεσε',text)) +'\n'
            text=text1+text2
        
        ## final list    
        if 'CRITICAL' in row[1]:
            critical.append([row[0],row[1],row[2],row[3],text])
        if 'MAJOR' in row[1]:
            major.append([row[0],row[1],row[2],row[3],text])

    

    string=''
    # if ctt has any other value other than None this table is created
    if not ctt == None: 
        string="|NTT Count|CTT Count|\n|----------|----------|\n"+"|"+ str(ntt) +"|"+ ctt +"|\n\n"
    
    # if there are no critical or major tickets the function returns
    if len(critical+major)==0:
        return( '[b]'+owner_group+'[/b]\n'+'ΔΕΝ ΥΠΑΡΧΟΥΝ ΕΚΚΡΕΜΟΤΗΤΕΣ')
        
    # bb code table initialization
    string = string + '\n[b]'+owner_group+'[/b]\n' + "|Ticket Νumber |Κρισιμότητα|Σύντομη Περιγραφή|Ομάδα Ανάθεσης|Σχόλια|\n|----------|----------|----------|----------|----------|\n"
    
    # converting list to string
    for row in critical + major:
        string+='|' +'|'.join(row)+'|\n'

    
    
    return string
    

### FIND LATEST CSV 
list_of_files = glob.glob('C:/Users/kpapaioa.TMNA/Downloads/*.csv') # * means all if need specific format then *.csv
latest_csv = max(list_of_files, key=os.path.getctime)
print("Importing: ",latest_csv)


### READ FROM CSV TO LIST
all_tickets=[]
with open(latest_csv,"r",encoding="utf-16") as f:       # read csv
    read=csv.reader(f, delimiter='\t',)
    
    for line in read:
        all_tickets.append(line)
        
### FIND THE INDEX OF THE NEEDED COLUMNS. (SR Number, Priority, Owner Group, Fault Synopsis, SR Comments)
for index,name in enumerate(all_tickets[0]):
    if 'SR Number' == name:     sr_col=index
    if 'Priority' == name:     pr_col=index
    if 'Owner Group' == name:    og_col=index
    if 'Fault Synopsis' == name:     fs_col=index
    if 'SR Comments' == name:    src_col=index


new_all_tickets=[]
for ticket in all_tickets:
    if 'MINOR' in ticket[4]:continue
    if 'WARNING' in ticket[4]:continue
    new_all_tickets.append([ticket[sr_col][2:],ticket[pr_col],ticket[og_col],ticket[fs_col],ticket[src_col]])
    


#ath=by_owner("NMC-DATA/IP",new_all_tickets,len(all_tickets),input('Ctt: '))
#thes=by_owner("NCC-THESS-DATA/IP",new_all_tickets,len(all_tickets))
#patr=by_owner("NCC-PATRA-DATA/IP",new_all_tickets,len(all_tickets))
#crete=by_owner("NCC-CRETE-DATA/IP",new_all_tickets,len(all_tickets))

#################################################

_1_ = ['08','09']
_2_ = ['14','15']
_3_ = ['22','23']
_4_ = ['06','07']

thes=by_owner("NCC-THESS-DATA/IP",new_all_tickets,len(all_tickets))
patr=by_owner("NCC-PATRA-DATA/IP",new_all_tickets,len(all_tickets))
crete=by_owner("NCC-CRETE-DATA/IP",new_all_tickets,len(all_tickets))



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
        thes=by_owner("NCC-THESS-DATA/IP",new_all_tickets,len(all_tickets))
        patr=by_owner("NCC-PATRA-DATA/IP",new_all_tickets,len(all_tickets))
        crete=by_owner("NCC-CRETE-DATA/IP",new_all_tickets,len(all_tickets))

        final=('[b]ΑΝΑΦΟΡΑ ΠΑΡΑΔΟΣΗΣ ΒΑΡΔΙΑΣ[/b]\n'+thes+patr+crete)
        break
    elif auto in _2_ or manual=='2':
        ath=by_owner("NMC-DATA/IP",new_all_tickets,len(all_tickets),input('Ctt: '))
        final=('[b]ΑΝΑΦΟΡΑ ΠΡΩΙΝΗΣ ΒΑΡΔΙΑΣ[/b]\n\n'+ath)
        break
    elif auto in _3_ or manual=='3':
        ath=by_owner("NMC-DATA/IP",new_all_tickets,len(all_tickets),input('Ctt: '))
        final=('[b]ΑΝΑΦΟΡΑ ΑΠΟΓΕΥΜΑΤΙΝΗΣ ΒΑΡΔΙΑΣ[/b]\n\n'+ath)
        break
    elif auto in _4_ or manual=='4':
        ath=by_owner("NMC-DATA/IP",new_all_tickets,len(all_tickets),input('Ctt: '))
        final=('[b]ΑΝΑΦΟΡΑ ΒΡΑΔΙΝΗΣ ΒΑΡΔΙΑΣ[/b]\n\n'+ath)
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
    
with open('report.txt',"w+",encoding='utf8') as file:
    file.write(final)
   
        

os.startfile('report.txt')

    