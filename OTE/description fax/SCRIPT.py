import sys, paramiko
import pandas as pd
import time
import warnings
import re
import os, datetime
warnings.filterwarnings("ignore")


def connect(server_ip,server_port,user,pswd):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)
    client.connect(server_ip, port=server_port, username=user, password=pswd)
    return(client)
    
def shelly(client):
    connection=client.invoke_shell()
    return (connection)

def cmd(connection, command,sec=0.5):
    connection.send(command +'\n')
    time.sleep(sec)
    output=connection.recv(4096)
    return output

def close(client):
    client.close()
    client.transport.close()
    del client
    return

#log.append([hostname, row.interface, row.old_desc,row.new_desc,xxx,www,m])



# TO EXCEL POU DIAVAZEI EXEI TA EKSIS COLUMNS
# 
df = pd.read_excel(io=input('Name of the file: ')+'.xlsx',reset_index=True) 
df.sort_values(by=['host'])
df = df[df.TODO=='do'].reset_index()
  


username = "kpapaioa"
password = 'k179350@K'
port = 22

log=[]

#  MAIN LOOP
hostname=''
for index,row in df.iterrows():
    
    www='N/A'
    xxx='N/A'
#    if index<=171:continue   #skiparei mexri tin seira 171
# CONNECTS TO NEW HOSTNAME
#    if hostname == row.host:continue
    if hostname!= row.host:
#        print(index)
        try:
            ssh.close()
            del ssh
        except:pass
        try:
            hostname=row.host
#            print('\n\n________________________\n\nThe following ',len(df[df.host==hostname]),' interfaces will be configured for ',hostname)   
#            print(df[df.host==hostname].interface.to_string())
#            if input('press enter to continue.. \n>>') != '':break
            print('\n\n Applying configurations for: ' +hostname)
            ssh=connect(hostname,port,username,password)
            shell=shelly(ssh)
        except:
            print('Could not connect to '+hostname+' !!')
            m='SSH_CONNECTION_FAILED'######################################################################################'CONNECTION_FAILED'
            log.append([hostname, row.interface,row.desc,www,m])
            hostname=''
            continue
        
        
        
#    try:    
    print(hostname,index,'/',len(df),'-',row.interface,end=':-')
    xx=cmd(shell, 'show run int ' +row.interface,2)
#    print(xx.decode())
    try:
        if 'No such configuration item' in xx.decode():
            m='INTERFACE_NOT_FOUND'#######################################################################################'INTERFACE_NOT_FOUND'
            log.append([hostname, row.interface,row.desc,www,m])
            print('> INTERFACE_NOT_FOUND', www)
            continue
       
        elif '\r\n description' in xx.decode() and '\r\n encapsulation'in xx.decode() :
#            H findall epistrefei lista. Emeis me to [0] kratame mono to 1o stoixeio tis listas
            xxx=re.findall(r'\r\n description (.*)\r\n encapsulation',xx.decode())[0]
        
            
        if len(xxx)<5:1/0 # if description is empty create error, to 1/0 trigarei errors
    except:
        print('> DESC_ERROR', www)
#        print(repr(xx.decode()))
        m='DESCRIPTION_ERROR'######################################################################################## OLD_DESCRIPTION_ERROR
        xxx='N/A'
        log.append([hostname, row.interface,row.desc,www,m])
        continue
#    www=xxx
#    ww=xx

    print(end='-')
    yy=cmd(shell, 'conf terminal')
    print(end='-')

    zz=cmd(shell, 'interface '+row.interface)
    print(end='-')

    aa=cmd(shell, 'description '+row.desc)
    print(end='-')

    ss=cmd(shell, 'commit')
    print(end='-')

    dd=cmd(shell, 'end') 
    print(end='-')

    ww=cmd(shell, 'show run int ' +row.interface,2)
#    print(ww.decode())
    try:
        if '\r\n description' in ww.decode() and '\r\n encapsulation'in ww.decode() :
            www=re.findall(r'\r\n description (.*)\r\n encapsulation',ww.decode())[0]
            
        if len(www)<5:1/0 # if description is empty create error
    except:
        print('> DESC_ERROR', www)
#        print(repr(ww.decode()))
        m='DESCRIPTION_ERROR'####################################################################################### NEW_DESCRIPTION_ERROR
        www='N/A'
        log.append([hostname, row.interface,row.desc,www,m])
        continue

        
#    Check status
    if row.desc in www or www in row.desc or row.desc in ww.decode():
        print('> SUCCESS  ',www)
        m='SUCCESS'#####################################################################################################SUCCESS
        log.append([hostname, row.interface,row.desc,www,m])
    else:
        print('> UNCONFIRMED  ',www)
        m='UNCONFIRMED'##################################################################################################### UNCONFIRMED
        log.append([hostname, row.interface,row.desc,www,m])
#    print(ww.decode())

try:
    ssh.close()
    del ssh
except:
    pass
print('Errors found: ',len(log))




df2 = pd.DataFrame(log)
out=input('enter output name: ')
df2.to_excel(excel_writer=out+'.xlsx',engine='xlsxwriter')
os.startfile(out+'.xlsx')



#log explanation
# hostname , interface , data_old_desc, data_new_description, machine_old_description, machine_new_description, message
#
# CONNECTION FAILED --> COULD NOT SSH TO MACHINE
#   INTERFACE_NOT_FOUND
#OLD_DESCRIPTION_ERROR
#NEW_DESCRIPTION_ERROR
#
#
#
#

