import datetime
import pandas as pd
import win32com.client
import time
import re



pd.options.display.max_colwidth = 100
ALL_CARDS=['NDLT-G', 'NDLT-J', 'NVLT-P', 'NTLT', 'NDPS', 'NANT','NALT-J', 'NVLT-P','NPOT-C',
           'ADLE', 'ADPD', 'ADEF', 'ADB', 'ASDA', 'ASRB', 'ASPB',
           'VPEA', 'VCMM',  'VDSH',  'VPEC', 'VCM', 'VDMF',
           'SDMM', 'SCUN', 'SDM', 'SCUK','SCUB',
           'DSRD','DSLD',
           'UP2A','UDMF',
           'CCUB','CCUC',
           'MVLT-D',
           'FCBC',
           'RDLT-C',
#           'FRAME','SFP','BACKPLANE','PAVDA',
#           'NDLT -G',
           ]

POWER_ONE=['XR08.48']

FAN_TRAY=['FAN TRAY']
SUBRACK=['SUBRACK']

PSU=['PAVDA']




###############################################################################
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6).Folders.Item("INVENTORY")
messages = inbox.Items#-----------------------------------------------INIT
messages.Sort("[ReceivedTime]", True)
message = messages.GetLast()#-----------------------------------------INIT
# TOTAL NUMBER OF EMAILS IN THE FOLDER
start_time = time.time()  


input("From date(dd/mm/yyyy): ")
messages = messages.Restrict("[ReceivedTime] > '" +frodate.format(datetime,'%m/%d/%Y')+"'")
input("To date(dd/mm/yyyy): ")
messages = messages.Restrict("[ReceivedTime] < '" +todate.format(datetime,'%m/%d/%Y')+"'")# %H:%M %p

print("Total messages: ",len(messages))




objects=[]
for message in messages:
    if message.subject.startswith('RE'):continue
    if message.subject.startswith('Απ:'):continue
    if 'ΑΚΥΡΩΣΗ' in message.body.upper():continue
    if not 'ΤΕΧΝΙΚΗ ΥΠΟΣΤΗΡΙΞΗ' in message.subject:continue
    for recipient in message.Recipients:
        if not 'DL-GRC01-Τμήμα Λειτουργίας Δικτύου Μετάδοσης' in str(recipient):continue 
    objects.append(message)   


class DSLAM():
    def __init__(self,x):
        self.name=''
        self.code=''
        self.brand=''
        self.text=x.upper().replace('/',' ').replace(' -',' ')
        self.flag=True
        
        self.cards=[]
        self.fans=[]
        self.subrack=[]
        self.power=[]
        self.co=0
        self.cc=0
        
        
        
        temp_name=''
        
        
        # NAME AND BRAND        
        for word in (self.text.split(' ')):            
            if '_ALU_' in word or '_ALC_' in word: 
                self.brand='Alcatel'
                temp_name=word
                
            elif '_HUA_' in word:
                self.brand='Huawei'
                temp_name=word
            elif 'RAYCAP' in word:
                self.brand='Raycap'
                temp_name='Raycap'
        if len(temp_name) < 4:
            temp_name=str(re.findall(r'DSLAM (\d{4}\d?) ',self.text))
            temp_name= 'DSLAM_'+temp_name
            
                
        # NAME
        self.name=temp_name.replace('\n','').replace(',','').replace('"','').replace(' ','')
        
        # CODE
        temp_code=re.findall(r'(\d{4}\d?)' ,self.name)
        if len(temp_code)>0:
            self.code=''.join(temp_code[0])
        else:
            self.code=''.join(temp_code)

        # CARD FINDERS
        for card in ALL_CARDS:
            if card in self.text and card not in self.cards:                
                self.cards.append(card.replace(' ',''))
                
        # POWER ONE FINDER
        for po in POWER_ONE:
            if po in self.text and po not in self.power:
                self.power.append(po)
                
        # FAN TRAY FINDER
        for fan in FAN_TRAY:        
            if fan in self.text and fan not in self.fans:
                self.fans.append(fan)
                
        # SUBRACK    
        for sub in SUBRACK:        
            if sub in self.text and sub not in self.subrack:
                self.fans.append(sub)
                
        self.cc=len(self.cards)+len(self.fans)+len(self.subrack)+len(self.power) + len(self.subrack)

                
        # THIS FLAG SHOWS IF THERE ARE ENTRIES IN INVENTORY
        if len(self.cards)==0 and len(self.fans)==0 and len(self.subrack)==0 and len(self.power)==0 and len(self.subrack)==0:
            self.flag=False
        
        
        
        
    def concatenate(self,y):
        self.cards+=(y.cards)
        self.fans+=(y.fans)
        self.subrack+=(y.subrack)
        self.power+=(y.power)
        self.text+=2*' ############################################################################# '+y.text
        self.co+=1
        self.cc+=len(y.cards)+len(y.fans)+len(y.subrack)+len(y.power) + len(y.subrack)
        

        
# DATASET MAKER IN DSL
temp=None            
dsl=[]
for i,obj in enumerate(objects):
    if 'subrack'.upper() in obj.body.upper():
        print('i')
#    print(i)
#    if  'ΑΝΤΙΚΑΤΆΣΤΑΣ' in obj.body.upper() and 'ΧΡΉΖΕΙ' in obj.body.upper():print('NAI')
    xx=obj.subject +' #!# ' + obj.body
    temp=DSLAM(xx)
    c=False
    for j,d in enumerate(dsl):
        if d.code==temp.code:
            d.concatenate(temp)
#            print(j,'aa          ',d.co)
            c=True
    if c:continue
    dsl.append(DSLAM(xx))
    
    
# VIEWS


# VIEW 1 - CARD FREQUENCY
card_counter=[]
for d in dsl:
    card_counter += d.cards
card_counter = {i:card_counter.count(i) for i in card_counter}
c_c=pd.DataFrame.from_dict(card_counter,orient='index').sort_values(by=[0], ascending=False)
c_c.to_excel(excel_writer=input('Type file name: ')+'.xlsx',engine='xlsxwriter',sheet_name='sheet1')



# VIEW 2 - DSLAM FREQUENCY
dslam_counter=[]
for d in dsl:
    if d.co > 0 and len(d.code)>4:
        dslam_counter.append(d.code +': Ord ('+ str(d.co) +'), Def ('+str(d.cc)+')' )      

input('Press enter to view per DSLAM')
for dd in dslam_counter:
    print(dd)


#for i,e in enumerate(dslam_counter):
#    sheet1.write(i,1,e)

# VIEW 3 - COUNTERs
input('Press enter to show fans etc...')
fan_counter=0
power_counter=0
subrack_counter=2
for d in dsl:
    fan_counter += len(d.fans)
    power_counter += len(d.power)
    subrack_counter += len(d.subrack)
    
print('fans= ',d.fans)
print('Power unit: = ',d.power)
print('subrack= ',d.subrack)

    
    



    
    




        
    
    

    
    
    
    
    
    
    
    