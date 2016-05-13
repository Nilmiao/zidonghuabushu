# -*- coding: utf-8 -*-
# deploy app system automatically
# before deployment, install putty first.(use it to copy directory to remote server)
from pyssh import PySSH
import os
import sys
import paramiko
import re

# set app package path
app_path = r'E:\test\html.zip'

# set the basic remote server info
hostname = '192.168.3.23'
username = 'root'
passwd = '123456'
idas_port = '8080'
wlan_port = '9020'
finance_port='8090'
tomcat_path = '/usr/local/tomcat'
app_name = 'html'
app_back_path = '/usr/local/projectback/html'
app_server_path = tomcat_path + '/webapps/' + app_name
app_config_path = app_server_path + '/js'
app_config_file1 = 'index.js'
#app_config_file2 = 'TrustMerchant.properties'


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
sftp.put(app_path, tomcat_path + '/webapps/' + app_name + '.zip')
sftp.close()
#sys.exit()
# unzip the <app_name>.war
#print ssh.runcmd('unzip ' + tomcat_path + '/webapps/' + app_name + '.war' + ' -d ' + tomcat_path + '/webapps/' + app_name
print ssh.runcmd('unzip ' + app_server_path + '.zip' + ' -d ' + app_server_path)
#+ ' -d ' + app_server_path
# copy the backup config files to the app path
print ssh.runcmd('rm -f ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
#print ssh.runcmd('rm -f ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
print ssh.runcmd('cp ' + app_back_path + '/' + app_config_file1 + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
## look up the wlan IP
print "looking up the wlan IP ..."
num = 5
wlan_ip = ''
while not wlan_ip and num > 0:
    #wlan_ip = ssh.runcmd('curl -s --connect-timeout 5 ifconfig.me/ip')
    wlan_ip = '171.221.151.66'
    if not wlan_ip:
        num = num - 1
        continue
    print wlan_ip
    pattern = re.compile("(\d+\.\d+\.\d+\.\d+)")
    res = pattern.search(wlan_ip).groups()
    wlan_ip = res[0]

    print ssh.runcmd('sed -i \'s/sharUrl\s*=.*/' + 'sharUrl=\"http:\/\/' + hostname + ':' + idas_port + '\/html\/shareindex\.html";\/\/' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')

    print ssh.runcmd('sed -i \'s/logoUrl\s*=.*/' + 'logoUrl=\"http:\/\/' + hostname + ':' + idas_port + '\/idas\/assets\/imgs\/logo\.jpg";\/\/' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')

# start tomcat 
print ssh.runcmd('/usr/local/tomcat/bin/startup.sh')

if not wlan_ip:
    print "cann't get wlan ip automatically, please get it manually"







