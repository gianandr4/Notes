import win32com.client
import xlwt

# EXCEL WORKBOOK INITIALIZATION 
book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")

# OUTLOOK INITIALIZATION
outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

# TO TARGET INBOX:inbox = outlook.GetDefaultFolder(6)      
# THIS TARGETS THE FOLDER CALLED BARBA                                       
inbox = outlook.GetDefaultFolder(6).Folders.Item("BARBA")
messages = inbox.Items#-----------------------------------------------INIT
message = messages.GetLast()#-----------------------------------------INIT
# TOTAL NUMBER OF EMAILS IN THE FOLDER
print("Total number",len(inbox.items))

month=map(int,(1,2,3,4,5,6,7,8,9,10,11,12))
search=input("Enter Month: (01-12):")

inp = input("Press Enter to continue...")
 
i=0
#sheet1.write(1, 0, send)
for message in messages:
    
    try:         
        if int(search) in month:
            msgr=str(message.Receivedtime)
            msgr, sep, tail = msgr.partition(' ')
            head, sep, msgr = msgr.partition('-')
            msgr, sep, tail = msgr.partition('-')
            if str(search)!=str(msgr):continue
        else:print("No filter")
        #if not mds.startswith('Automatic addition'):continue   ###show only mails with...
        
        print(message.ReceivedTime)
        sheet1.write(i, 3,str(message.ReceivedTime)) 
        
        print(str(message.body))
        sheet1.write(i, 2, str(message.body))
        
        print(str(message.Subject))
        sheet1.write(i, 1, message.Subject)
        
        if message.SenderEmailType == "EX":
            print(message.Sender.GetExchangeUser().PrimarySmtpAddress)
            sheet1.write(i, 0, str(message.Sender.GetExchangeUser().PrimarySmtpAddress))
        elif message.SenderEmailType == "SMTP":
            print(message.SenderEmailAddress)
            sheet1.write(i, 0, str(message.SenderEmailAddress))
        
        i=i+1
        if i%100==0:
            print("\nCount= ",i)
            inp = input("Press Enter to continue...")
        if inp == "stop":
            break
    except:continue



print("\nTotal Count= ",i)
book.save("trial25.xls")

    
    
    
    
    
    
    
    
    
    
    
    
"""
    if message.SenderEmailType == "EX":
        print(message.Sender.GetExchangeUser().PrimarySmtpAddress)
    elif message.SenderEmailType == "SMTP":
        print(message.SenderEmailAddress)
    else:
        continue
      
    msgr=str(message.Receivedtime)
    msgr, sep, tail = msgr.partition(' ')
    head, sep, msgr = msgr.partition('-')
    msgr, sep, tail = msgr.partition('-')
    if str(x)!=str(msgr):
        continue
        
  
    

        
   

#IP_PROHELPER - WORKS
#BARBA -ERROR BECAUSE OF A DELETED MAIL
#
#








# SUBJECT -  EASY - WORKS
# READ ALL SUBJ AND SAVE THEM TO EXCEL


i=1
for message in messages:
    print(message.subject)
    print(i)
    i=i+1
    
print (i)    



# BODY -  HARD - NO (BREAKS AT 35)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# READ ALL BODY AND SAVE THEM TO EXCEL

i=1
for message in messages:
    print (str(message.body))
    print(i)
    i=i+1
    
print (i)   



# MAIL -  MEDIUM - NO (BREAKS AT 35)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# READ ALL MAIL ADDRESSES AND SAVE THEM TO EXCEL

i=1
for message in messages:
    if len(message.Sender.GetExchangeUser().PrimarySmtpAddress)<len(message.SenderEmailAddress):
        print(message.Sender.GetExchangeUser().PrimarySmtpAddress)
    else:
        print(message.SenderEmailAddress)
    print(i)
    i=i+1
       
print(i)


# DATE -  MEDIUM - NO (BREAKS AT 35)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# READ ALL DATE AND TIME AND SAVE THEM TO EXCEL

i=1
for message in messages:
    print(message.ReceivedTime)
    print(i)
    i=i+1
    
    
"""    
    
    
    
    
    
    
    
    
    
    