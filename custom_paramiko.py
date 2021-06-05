import paramiko
import time

def connect(server_ip,server_port,user,pswd):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)
    client.connect(server_ip, port=server_port, username=user, password=pswd)
    return(client)
    
def shell(client):
    connection=client.invoke_shell()
    return (connection)

def cmd(connection, command,sec=0.5):
    connection.send(command +'\n')
    time.sleep(sec)
    output=connection.recv(4096)
    return output

def close(client):
    client.close()
    return







#
#
#
#
#    
#    
#
#hostname = 'acha9010a'
#password = 'Th@654321!'
##command = 'show run int'
#username = "itheodosis"
#port = 22
#interface='TenGigE0/1/0/7.1204'
#desc='|ELINE|21A1041233|GERMANOS_PL.EIRHNHS-AXARNON_1ST,NO_NTE_VLAN1204|'
#
#
#
#ssh=connect(hostname,port,username,password)
#shell=shell(ssh)
#
#xx=cmd(shell, 'show run int ' +interface,2)
#print(xx.decode())
#yy=cmd(shell, 'conf terminal')
#zz=cmd(shell, 'interface '+interface)
#aa=cmd(shell, 'description '+desc)
#ss=cmd(shell, 'commit')
#dd=cmd(shell, 'end')
#ww=cmd(shell, 'show run int ' +interface,2)
#print(ww.decode())
#
#
#
#
#
#
#close(ssh)
