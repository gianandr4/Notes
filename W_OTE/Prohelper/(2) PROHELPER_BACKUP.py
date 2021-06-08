import win32com.client
import xlwt
from datetime import datetime


class devices():
    def __init__(self,subj):
        self.added=0
        self.failed=0
        self.name=""
        self.subj=subj
        self.MW=0

#---Those are functions that extract the device names from the mail subject---#
#---Splits string to 3 parts(head,sep,tail) and you can use each one of them--#
    def Convert_device_Added(self):
        device, sep, tail = self.subj.partition(" in ") #remove shit
        device, sep, tail = tail.partition(" due ") # date time split
        return(device)
        
    def Convert_device_Failed(self):
        device, sep, tail = self.subj.partition(" for ") #remove shit
        device, sep, tail = tail.partition(". ") # date time split
        if device=="":
            head, sep, device = self.subj.partition(" in ") #specific case
            if len(device)>11:device, sep, tail = device.partition(".")#more specific
        return(device)
        
    def Convert_device_MW(self):
        head, sep, device = self.subj.partition("in ") #remove shit
        return(device)
        

#    
#def Get_Convert_Date(date):
#    date=str(date)
#    date, sep, time = date.partition(" ") # date time split
#    date=date.replace("-","")#clean date
#    return(date)
                 
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("test")
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6).Folders.Item("IP_PROHELPER")
messages = inbox.Items
message = messages.GetLast()
  


devlist=[]
Ename=0
Exists=False


print("PROHELPER \n----\n")
input("From date(dd/mm/yyyy): ")
messages = messages.Restrict("[ReceivedTime] >= '" +frodate.format(datetime,'%m/%d/%Y %H:%M %p')+"'")
input("To date(dd/mm/yyyy): ")
messages = messages.Restrict("[ReceivedTime] <= '" +todate.format(datetime,'%m/%d/%Y %H:%M %p')+"'")
print("Total messages: ",len(messages),'from: ',frodate,'to',todate,'\n\n')
    
rt=message.receivedtime

messages.Sort("[ReceivedTime]", False)
for message in messages:
    if message.receivedtime<rt:
        print(message.receivedtime)
    
    E=devices(message.subject)
    if message.subject.startswith('Automatic addition'):
        Ename=E.Convert_device_Added()
        for device in devlist:
            Exists=False
            if Ename == device.name:                    
                Exists=True
                device.added +=1
                break
        if not Exists:
            devlist.append(devices(message.subject))
            devlist[-1].name=Ename
            devlist[-1].added +=1
            
    elif message.subject.startswith('Failure'):
        Ename=E.Convert_device_Failed()
        for device in devlist:
            Exists=False
            if Ename == device.name:                    
                Exists=True
                device.failed +=1
                break
    elif not Exists:
            devlist.append(devices(message.subject))
            devlist[-1].name=Ename
            devlist[-1].failed +=1

#333333333333333333333333333333333333333333333333333333             
    elif message.subject.startswith('MW'):
        Ename=E.Convert_device_MW()
        for device in devlist:
            Exists=False
            if Ename == device.name:                    
                Exists=True
                device.MW +=1
                break
        if not Exists:
            devlist.append(devices(message.subject))
            devlist[-1].name=Ename
            devlist[-1].MW +=1
#44444444444444444444444444444444444444444444444444444444444444                
    else:
        print(message.receivedtime, message.subject)
    rt=message.receivedtime
        

            
            



  



i=0  
sheet1.write(0, 1, "DEVICE NAME")
sheet1.write(0, 2, "ADDED POOLS")
sheet1.write(0, 3, "MW")
sheet1.write(0, 4, "FAILED")
sheet1.write(0, 6, "TOTAL(MW + ADDED)")


ii=[]


for j,devices in enumerate(devlist):
    i+=1
    ii.append([devices.name, devices.added, devices.MW, devices.failed, devices.added + devices.MW])
    
    sheet1.write(i, 1, devices.name)
    sheet1.write(i, 2, devices.added)
    sheet1.write(i, 3, devices.MW)
    sheet1.write(i, 4, devices.failed)
    sheet1.write(i, 6, devices.added + devices.MW)
    
    
p=i+2
sum_added=0
sum_mw=0
sum_failed=0
sum_added_mw=0
for devices in devlist:
    sum_added+=devices.added
    sum_mw+=devices.MW
    sum_failed+=devices.failed
    sum_added_mw+=devices.added + devices.MW

 
sheet1.write(p+2,0,len(devlist))    
sheet1.write(p+1,0,'NODES')

sheet1.write(p+2,1,sum_added)
sheet1.write(p+1,1,'ADDED POOLS')

sheet1.write(p+2,2,sum_mw)
sheet1.write(p+1,2,'MW')


sheet1.write(p+2,3,sum_failed)
sheet1.write(p+1,3,'FAILED')

sheet1.write(p+2,4,sum_added_mw)
sheet1.write(p+1,4,'TOTAL(MW + ADDED)')

    
path_name=input("Give Excel save path: ")
if ".xls" not in path_name:path_name+=".xls"
book.save(path_name)
            




    


        
    
    
    
    











