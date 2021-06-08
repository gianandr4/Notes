import tkinter as tk
import os
#import ssh2
import socket
from ssh2.session import Session
import re
import pandas as pd
from datetime import datetime
import sys

paths=("""
Root path:
  
|Machine Logs 
|__Cisco
   |__info.log
   |__debug.log
   |__critical.log
|__Huawei(9306)
   |__info.log
|ACS (Tacaccs) 
|__Cisco
   |__tacacct.log
|__Huawei(9306)
   |__tacacct.log
|__Huawei other
   |__info.log""")
#print (paths)
def show_entry_fields():
#   sys.stderr.write("\x1b[2J\x1b[H")
   U=Username.get()# USERNAME
   P=Password.get()# PASSWORD
   H=Hostname.get()# DEVICE HOSTNAME
   L=log.get()# EVENT LOG OR ACS LOG
   D=device.get()# CISCO HUAWEI(9306)
#   T=typ.get()# INFO CRITICAL TACCACCT DEBUG
   M=mon.get()# MONTH
   Day=day.get()# DAY
   K=Keywords.get()#keywords
   T=''
############################################################################### LOGIN
   host='79.128.180.20'   
   H=H.replace(' ','')
   if len(H)==0:
       print('\nEnter a Hostname...\n')
       return
   if len(K)>0:
       K='|'+K.replace(' ',' |')
   


   try: 
       sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       sock.connect((host,22)) #host/port
       #start session
       session = Session()
       session.handshake(sock)
       session.userauth_password(U,P)
       channel= session.open_session()
       print('Login Successful!!!\n')
   except:
       print('WRONG CREDENTIALS\n')
       return
   
       
   channel.shell()   
   
   channel.write('host '+H+'\n')
   size,data = channel.read()
   ip= re.findall(r'(\d{2}.\d{1}\d?\d?.\d{1}\d?\d?.\d{1}\d?\d?)',str(data))
   print(data.decode())
   if 'not found:' in data.decode():
       return





############################################################################### PATHFINDER
   H=' '+H+' '
   if L == "Machine Logs":
       command = K
       if D == 'Cisco':
#           if T == 'Tacacct':#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#               print('Wrong input--> Type')
#               return
               
           print('>>>','cd /netlog/cisco')
           channel.write('cd /netlog/cisco\n')
       elif not D == 'Cisco' :
           T='info'
#           if not T== 'Info':#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#               print('Wrong input--> Type')
#               return
           
           print('>>>','cd /netlog/misco')
           channel.write('cd /netlog/misco\n')
           
       print('>>>','ls -lt')
       channel.write('ls -lt\n')   
#################################################################################################           
       
   elif L == "ACS (Tacaccs)":
#       check the condidions that do not work with
       #GET IP FROM HOSTNAME

       HH=H       
       if D == 'Cisco' :
           H=" '"+ip[0]+",' "
           command = r''' | awk -F"atheacs|CmdSet=|RequestLatency|User=|Port=" '/CmdAV/ {print$1$5$3}'| egrep -v "acctman|scriptman" | grep CmdAV | more'''
#           if not T == 'Tacacct':#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#               print('Wrong input--> Type')
#               return
           T='tacacct'
           print('>>>','cd /netlog/acslogs')
           channel.write('cd /netlog/acslogs\n')
           
       elif D == 'Huawei 9306':
           H=" '"+ip[0]+",' "
           command = r''' | awk -F"atheacs|CmdSet=|RequestLatency|User=|Authen-Method=|Protocol" '/CmdAV/ {print$1$6$3}' | egrep -v "acctman|scriptman" | grep CmdAV | more'''
#           if not T == 'Tacacct':#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#               print('Wrong input--> Type')
#               return
           T='tacacct'
           print('>>>','cd /netlog/acslogs')
           channel.write('cd /netlog/acslogs\n')

       elif D == 'Huawei':
           command = r''' | awk -F":" '/command/ {printf"%s-%s-%s %s -> %s %s \n",$1,$2,$6,$7,$8,$9}' | more'''
#           if not T == 'Info':#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#               print('Wrong input--> Type')
#               return          
           T='info'
           print('>>>','cd /netlog/misco')
           channel.write('cd /netlog/misco\n')

       print('>>>','ls -lt')
       channel.write('ls -lt\n')


  

#
################################################################################ GIVE COMMAND AND EXPORT
  #       READ FROM SCREEN AND CREATE STRING NAMED TEXT
   text=''
   count=0
   buffer=1024
   while True:
       size, data = channel.read(buffer)
       text+=str(data.decode())
       count+=int(size)
       if size<buffer:break 
#   print(text)


   text=re.sub(' +', ' ', text).strip()#remove blanks
   df = pd.DataFrame([x.split(' ') for x in text.split('\n')]).dropna()
   df=df[[3,5,6,7,8]]
   df=df.rename(columns={3: "Type", 5: "Month", 6:"Day", 7:"Time", 8:"File_name"})   
   

   try:       
       df2=df.loc[(df['Month'] == M ).reset_index(drop=True) & (df['Day']==Day)& (df["File_name"].str.contains(T.lower())) ].reset_index(drop=True)#month date and type ||
   except:
       print('\nNo records for',M,Day,'-->',T+'.log')
       return
   
   ij=0
   if len(df2)>1:
       print('\nSelect file\n',df2)

       while True:
               ij = input("Please enter a number: ")
               try:
                   if ij=='':
                       print('Canceled..\n\n')
                       return
                   elif int(ij) >= 0 and int(ij)<=(len(df2)-1):
                       break

               except:
                   print ('\nInvalid input. Please select a number between 0 and',len(df2)-1)
               
           
           
   print('Opening: ',df2.at[int(ij),'File_name'])
   string=df2.at[int(ij),'File_name']
   
   if '.gz' in string:
       c1='zgrep'
   else:
       c1='grep'
   
   final_command=c1+H+string+command
   print('\n>>>',final_command)

   channel.write(final_command+'\n')
   channel.write('date\n')


   


   
   text=''
   count=0
   buffer=4096
   while True:
       size, data = channel.read(buffer)
       text+=str(data.decode())
       count+=int(size)
       print('reading:',count)
       if size<buffer:
           print('reading complete..')
           break    
   text=text.replace('CmdAV=','')
   text=text.replace('CmdArgAV=','')
   text=text.replace('<cr>','')

   text_file = open("out.txt", "w")
   text_file.write(text)
   text_file.close()
   os.startfile("out.txt")
   #read and open txt  
       

       
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   

# LABELS FOR CREDENTIALS
master = tk.Tk()

tk.Label(master, text="Username").grid(row=0,column=0)
Username = tk.Entry(master)
Username.grid(row=0, column=1)

tk.Label(master, text="Password").grid(row=1, column=0)
Password = tk.Entry(master, show="*")
Password.grid(row=1, column=1) 

# CHECK CREDENTIALS BUTTON
#tk.Button(master, text='Show', command=show_entry_fields).grid(row=2, column=1, sticky=tk.W, pady=4)
tk.Label(master, text="______________________________________").grid(row=2,columnspan=10)

tk.Label(master, text="Hostname").grid(row=3,column=0)
Hostname = tk.Entry(master)
Hostname.grid(row=3, column=1)

# DROP DOWN FOR LOG 
tk.Label(master, text="Log:").grid(row=4,column=0)
log = tk.StringVar(master)
log.set("ACS (Tacaccs)") # default value
w = tk.OptionMenu(master, log, "Machine Logs", "ACS (Tacaccs)")
w.grid(row=5, column=0)   


# DROP DOWN FOR DEVICE
tk.Label(master, text="Device:").grid(row=4,column=1)
device = tk.StringVar(master)
device.set("Cisco") # default value
w = tk.OptionMenu(master, device, "Cisco", "Huawei 9306", "Huawei")
w.grid(row=5, column=1)   

# DROP DOWN FOR TYPE
#tk.Label(master, text="Type:").grid(row=4,column=2)
#typ = tk.StringVar(master)
#typ.set("Info") # default value
#w = tk.OptionMenu(master, typ, "Info", "Critical", "Tacacct", "Debug")
#w.grid(row=5, column=2) 


#if typ.get() =='Info':
# DROP DOWN FOR MONTH
tk.Label(master, text="Month:").grid(row=6,column=0)
mon = tk.StringVar(master)
mon.set(datetime.now().strftime('%b')) # default value
w = tk.OptionMenu(master, mon, "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
w.grid(row=7, column=0) 

# DROP DOWN FOR DAY
tk.Label(master, text="Day:").grid(row=6,column=1)
day = tk.StringVar(master)
day.set(datetime.now().strftime('%d').replace('0','')) # default value
w = tk.OptionMenu(master, day, "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30","31")
w.grid(row=7, column=1) 

tk.Label(master, text="                                      ").grid(row=8,columnspan=10)


tk.Label(master, text="Keywords").grid(row=9,column=0)
Keywords = tk.Entry(master)
Keywords.grid(row=9, column=1)

tk.Label(master, text="______________________________________").grid(row=10,columnspan=10)

tk.Button(master, text='Show logs', command=show_entry_fields).grid(row=11, column=1, sticky=tk.W, pady=4)


tk.mainloop()
