# -*- coding: utf-8 -*-
# deploy boss system automatically
from pyssh import PySSH
import os
import sys
import paramiko
import re

# set app package path
app_path = r'E:\test\boss.war'

# set the basic remote server info
hostname = '192.168.3.23'
username = 'root'
passwd = '123456'
idas_port = '8080'
wlan_port = '9020'
finance_port='8090'
tomcat_path = '/usr/local/tomcat'
app_name = 'boss'
app_back_path = '/usr/local/projectback/boss'
app_server_path = tomcat_path + '/webapps/' + app_name
app_config_path = app_server_path + '/WEB-INF/classes'
app_config_path1 = app_server_path + '/js/lib/ueditor'
app_config_file1 = 'projectUrl.properties'
app_config_file2 = 'umeditor.config.js'
app_config_file3 = 'oracle_db.properties'


# connect to the server
ssh = PySSH()
ssh.connect(hostname, username, passwd)

# output the date
print ssh.runcmd('date').decode('UTF-8')

# shutdown tomcat
print ssh.runcmd('/usr/local/tomcat/bin/shutdown.sh').decode('UTF-8')

# delete all tomcat cache
print ssh.runcmd('rm -rf /usr/local/tomcat/work/*').decode('UTF-8')

# copy new app package to the server
#print os.system('scp  ' + '"' + app_path + '"' + username + '@' + hostname + ':' + tomcat_path + '/webapps/')
#copy_cmd =  'pscp -l ' + username + ' -pw ' + passwd + ' ' + '"' + app_path + '"' + ' ' + hostname + ':' + tomcat_path + '/webapps/'
#print copy_cmd
#print os.system(copy_cmd)
client = paramiko.SSHClient()
#Don't use host key auto add policy for production servers
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.load_system_host_keys()
try:
    client.connect(hostname, 22, username, passwd)
except (socket.error,paramiko.AuthenticationException) as message:
    print "ERROR: SSH connection to "+ hostname + " failed: " + str(message)
    sys.exit(1)
sftp = client.open_sftp()
sftp.put(app_path, tomcat_path + '/webapps/' + app_name + '.war')
sftp.close()
#sys.exit()

# delete app directory 
#print ssh.runcmd('rm -rf ' + tomcat_path + '/webapps/' + app_name)
print ssh.runcmd('rm -rf ' + app_server_path)

# unzip the <app_name>.war
#print ssh.runcmd('unzip ' + tomcat_path + '/webapps/' + app_name + '.war' + ' -d ' + tomcat_path + '/webapps/' + app_name)
print ssh.runcmd('unzip ' + app_server_path + '.war' + ' -d ' + app_server_path)

# copy the backup config files to the app path
print ssh.runcmd('rm -f ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
#print ssh.runcmd('rm -f ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
print ssh.runcmd('cp ' + app_back_path + '/' + app_config_file1 + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
print ssh.runcmd('cp ' + app_back_path + '/' + app_config_file3 + ' ' + app_config_path + '/' + app_config_file3).decode('UTF-8')

## look up the wlan IP
print "looking up the wlan IP ..."
num = 5
wlan_ip = ''
while not wlan_ip and num > 0:
    #wlan_ip = ssh.runcmd('curl -s --connect-timeout 10 ifconfig.me/ip')
    wlan_ip = '171.221.151.66'
    #wlan_ip = '1.1.1.1'
    if not wlan_ip:
        num = num - 1
        continue
    print wlan_ip
    pattern = re.compile("(\d+\.\d+\.\d+\.\d+)")
    res = pattern.search(wlan_ip).groups()
    wlan_ip = res[0]
  #cmd1 = 'sed -i \'s/^share_collective_url=.*/' + 'share_collective_url=http:\/\/' + wlan_ip + ':' + wlan_port + '\/idas\/share\/collectiveDraving?collectiveDravingId=' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1
#    #print cmd1
    print ssh.runcmd('sed -i \'s/accessUrl=.*/' + 'accessUrl=http\\:\/\/' + hostname + '\\:' + idas_port + '\/' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    print ssh.runcmd('sed -i \'s/storageUrl=.*/' + 'storageUrl=\/usr\/local\/tomcat\/webapps' + '\/' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    ###########################财务系统接口########################
    print ssh.runcmd('sed -i \'s/pay_url\s*=.*/' + 'pay_url=http:\/\/' + hostname + ':' + finance_port + '\/finance\/dispatch\/dispatch.action' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')

# start tomcat 
print ssh.runcmd('/usr/local/tomcat/bin/startup.sh').decode('UTF-8')

if not wlan_ip:
    print "cann't get wlan ip automatically, please get it manually"




