import os
#import ssh2
import socket
from ssh2.session import Session
import re
from datetime import datetime
import sys



#

U=sys.argv[1] # USERNAME
P=sys.argv[2] # PASSWORD
arg=sys.argv[3] # CHOSEN STRING
K=sys.argv[4] # KEYWORDS



U='kpapaioa'
P='Mm153650!'
arg='2)_31_Jan_2019_(ac)_nyma-asr9ka__tacacct.log.366.gz'





arg=arg.replace('__','_')
arg=arg.split('_')


for i in range(1):
    if len(arg)<7:
        print('Error, invalid argument')
        break
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host,22)) #host/port
        #start session
        session = Session()
        session.handshake(sock)
        session.userauth_password(U,P)
        channel= session.open_session()
    except:
        print('WRONG CREDENTIALS\n')
        break    
    
    channel.shell()   
    cat=arg[4]
    H=arg[5]
    F=arg[6]
    
    # find ip
    ip=''
    channel.write('host '+H+'\n')
    size,data = channel.read()
    ip= re.findall(r'(\d{2}.\d{1}\d?\d?.\d{1}\d?\d?.\d{1}\d?\d?)',str(data))[0]
    if 'not found:' in data.decode():
        print('UNKNOWN HOSTNAME')
        break
    
    
    if '.gz' in F:
        command='zgrep '
    else:
        command='grep ' 
        
    
    if 'ce' in cat:#CISCO EVENT LOGS  (cd /netlog/cisco)    
        command+= H+' /netlog/cisco/'+F    
    elif 'me' in cat:    #MISCO EVENT LOGS HUA OTHER (cd /netlog/misco)
        command+= H+' /netlog/misco/'+F
    elif 'mo' in cat:    #MISCO EVENT LOGS HUA 9300 (cd /netlog/misco)
        command+= H+' /netlog/misco/'+F
        
    
    elif 'ac' in cat:    #ACS TACACCTS CISCO (cd /netlog/acslogs)
        command+= ip +' /netlog/acslogs/'+ F +r''' | awk -F"atheacs|CmdSet=|RequestLatency|User=|Port=" '/CmdAV/ {print$1$5$3}'| egrep -v "acctman|scriptman" | grep CmdAV'''
    elif 'mt' in cat:    #TACACCTS HUA OTHER (cd /netlog/misco)
        command= H +' /netlog/misco/'+ F +r''' | awk -F"atheacs|CmdSet=|RequestLatency|User=|Authen-Method=|Protocol" '/CmdAV/ {print$1$6$3}' | egrep -v "acctman|scriptman" | grep CmdAV'''
    elif 'ah' in cat:    #ACS TACACCTS HUA 9300 (cd /netlog/acslogs)
        command= ip +''' /netlog/acslogs/'+ F +r' | awk -F"%%|User=|Command=" '/Command/ {print$1$3$4}' '''
    
    
    print (command)
    
#    break
    channel.write(command + '\n')
    channel.write('date\n')
            
    text=''
    while True:
        size, data = channel.read(4096)
        text+=str(data.decode())
        if size<4096:
            break    
        
    text=text.replace('CmdAV=','')
    text=text.replace('CmdArgAV=','')
    text=text.replace('<cr>','')

    
    
    
    
channel.close()


print(text)




















#
#
#
#
#for i in range(1):
################## CREDENTIALS AND HOSTNAME CHECK    
#    if len(H)==0:
#        print('\nEnter a Hostname...\n')
#        break
################## SSH Connection 
#   
#    try:
#        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        sock.connect((host,22)) #host/port
#        #start session
#        session = Session()
#        session.handshake(sock)
#        session.userauth_password(U,P)
#        channel= session.open_session()
#    except:
#        print('WRONG CREDENTIALS\n')
#        break
#   
################ IP finder       
#    channel.shell()   
#   
#    channel.write('host ' + H + '\n')
#    size,data = channel.read()
#    ip= re.findall(r'(\d{1}\d?\d?.\d{1}\d?\d?.\d{1}\d?\d?.\d{1}\d?\d?)',str(data.decode()))[0]
#    
#    print(ip)
#    if 'not found:' in data.decode():
#        print('UNKNOWN HOSTNAME')
#        break
#        
#        
#    #CISCO EVENT LOGS  (cd /netlog/cisco)  
#    ce=''
#    #MISCO EVENT LOGS HUA OTHER (cd /netlog/misco)
#    me=''
#    #MISCO EVENT LOGS HUA 9300 (cd /netlog/misco)
#    mo=''
#    
#    #ACS TACACCTS CISCO (cd /netlog/acslogs)
#    ac=r''' | awk -F"atheacs|CmdSet=|RequestLatency|User=|Port=" '/CmdAV/ {print$1$5$3}'| egrep -v "acctman|scriptman" | grep CmdAV | more'''
#    #TACACCTS HUA OTHER (cd /netlog/misco)
#    mt=r''' | awk -F":" '/command/ {printf"%s-%s-%s %s -> %s %s \n",$1,$2,$6,$7,$8,$9}' | more'''
#    #ACS TACACCTS HUA 9300 (cd /netlog/acslogs)
#    ah=r''' | awk -F"atheacs|CmdSet=|RequestLatency|User=|Authen-Method=|Protocol" '/CmdAV/ {print$1$6$3}' | egrep -v "acctman|scriptman" | grep CmdAV | more'''
#    
#    
#    final=''
#    Filter=''
#    
#    # L = Event, Tacacct
#    # D= Cisco, Huawei_Other, Huawei_9300
#    
#    
#    if L=='Event' and D=='Cisco':
#        final='(ce)'
#        channel.write('cd /netlog/cisco\n')
#        
#    elif L=='Event' and D=='Huawei_Other':
#        final='(me)'
#        channel.write('cd /netlog/misco\n')
#        
#    elif L=='Event' and D=='Huawei_9300':
#        final='(mo)'
#        channel.write('cd /netlog/misco\n')
#        
#    elif L=='Tacacct' and D=='Cisco':
#        final='(ac)'
#        channel.write('cd /netlog/acslogs\n')
#        Filter='|grep tacacct'
#        
#    elif L=='Tacacct' and D=='Huawei_Other':
#        final='(mt)'
#        channel.write('cd /netlog/misco\n')
#        Filter='|grep tacacct'
#
#        
#    elif L=='Tacacct' and D=='Huawei_9300':
#        final='(ah)'
#        channel.write('cd /netlog/acslogs\n')
#        Filter='|grep tacacct'
#        
#    channel.write('ls -lt'+ Filter +'\n')
#
#    text=''
#    while True:
#        size, data = channel.read(1024)
#        text+=str(data.decode())
#        if size<1024:break 
#    
#    
#    
#    
#       
#    text=re.sub(' +', ' ', text).strip()#remove blanks
#    loggg=text.splitlines()
#    final_log=[]
#   
#    for logg in loggg:
#        logg= logg.split(' ')
##        asda.append([logg[5],logg[6],logg[7],logg[8]])
#        if len(logg)==9:
##           print(logg[5],logg[6],logg[7],logg[8])
#            if logg[5]==M:
#                if logg[6]==Day:
#                   
#                    final_log.append([logg[5],logg[6],logg[7],logg[8]])
#    if len(final_log)==0:
#        print('No logs found for that date')
#        break
#    else:
#        final_string=''
#        for i,temp in enumerate(final_log):
#            final_string+=str(i)+')_'+temp[1]+'_'+temp[0]+'_'+temp[2]+'_'+final+'_'+temp[3]+'\n'
#    print(final_string)
#channel.close()
#
#    


    
    
        
    

        
    










































