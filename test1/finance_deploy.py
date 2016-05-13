# -*- coding: utf-8 -*-
# deploy app system automatically
from pyssh import PySSH
import os
import sys
import paramiko
import re

# set app package path 
app_path = r'E:\test\finance.war'
#app_path = r'E:\qttecx\svn_code\ÎÝÍÐ°î\V2.0\07 ×ª²âÊÔ\V2.1M01R10\idas.war'
#app_path = r'E:\qttecx\svn_code\ÎÝÍÐ°î\V2.0\07 ×ª²âÊÔ\V2.1M01R04\idas.war'

# set the basic remote server info
hostname = '192.168.3.23'
username = 'root'
passwd = '123456'
wlan_port = '9020'
idas_port = '8080'
finance_wlan_port = '9120'
finance_port='8090'
tomcat_path = '/usr/local/finance'
app_name = 'finance'
app_back_path = '/usr/local/projectback/finance'
app_server_path = tomcat_path + '/webapps/' + app_name
app_config_path = app_server_path + '/WEB-INF/classes'
app_config_file1 = 'projectUrl.properties'
app_config_file2 = 'TrustMerchant.properties'
app_config_file3 = 'acp_sdk.properties'
app_config_file4 = 'oracle_db.properties'
app_config_file5 = 'abc'
app_config_file6 = 'icbc'
app_config_file7 = 'union'
app_config_file8 = 'wx'

# connect to the server
ssh = PySSH()
ssh.connect(hostname, username, passwd)

# output the date
print ssh.runcmd('date').decode('UTF-8')

# shutdown tomcat
print ssh.runcmd('/usr/local/finance/bin/shutdown.sh').decode('UTF-8')


# delete all tomcat cache
print ssh.runcmd('rm -rf /usr/local/finance/webapps/finance.war').decode('UTF-8')

print ssh.runcmd('rm -rf /usr/local/finance/work/*').decode('UTF-8')

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
sftp.put(app_path, app_server_path + '.war')
sftp.close()
#sys.exit()

# delete app directory 
#print ssh.runcmd('rm -rf ' + tomcat_path + '/webapps/' + app_name)
print ssh.runcmd('rm -rf ' + tomcat_path + '/webapps/' + app_name)
# unzip the app package
#print ssh.runcmd('unzip ' + tomcat_path + '/webapps/' + app_name + '.war' + ' -d ' + tomcat_path + '/webapps/' + app_name)
print ssh.runcmd('unzip ' + app_server_path + '.war' + ' -d ' + app_server_path).decode('UTF-8')

# copy the backup config files to the app path
print ssh.runcmd('rm -f ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
print ssh.runcmd('rm -f ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
print ssh.runcmd('rm -f ' + app_config_path + '/' + app_config_file3).decode('UTF-8')
print ssh.runcmd('cp ' + app_back_path + '/' + app_config_file1 + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
print ssh.runcmd('cp ' + app_back_path + '/' + app_config_file2 + ' ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
print ssh.runcmd('cp ' + app_back_path + '/' + app_config_file3 + ' ' + app_config_path + '/' + app_config_file3).decode('UTF-8')
print ssh.runcmd('cp ' + app_back_path + '/' + app_config_file4 + ' ' + app_config_path + '/' + app_config_file4).decode('UTF-8')
print ssh.runcmd('cp ' + app_back_path + '/' + app_config_file5 + ' ' + app_config_path + '/' + app_config_file5).decode('UTF-8')
print ssh.runcmd('cp ' + app_back_path + '/' + app_config_file6 + ' ' + app_config_path + '/' + app_config_file6).decode('UTF-8')
print ssh.runcmd('cp ' + app_back_path + '/' + app_config_file7 + ' ' + app_config_path + '/' + app_config_file7).decode('UTF-8')
print ssh.runcmd('cp ' + app_back_path + '/' + app_config_file8 + ' ' + app_config_path + '/' + app_config_file8).decode('UTF-8')

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
    #######################农行支付请求url#################
    #print ssh.runcmd('sed -i \'s/abc_pay_url\s*=.*/' + 'abc_pay_url=http:\/\/' + wlan_ip + ':' + wlan_port + '\/idas\/abc\/MerchantPayment' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    #######################工行支付请求url#################
    #print ssh.runcmd('sed -i \'s/icbc_pay_url\s*=.*/' + 'icbc_pay_url=http:\/\/' + wlan_ip + ':' + wlan_port + '\/idas\/icbc\/submittran' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    #####################工行支付回调IP########################
    print ssh.runcmd('sed -i \'s/icbc_pay_callback_url\s*=.*/' + 'icbc_pay_callback_url=http:\/\/' + wlan_ip + ':' + finance_wlan_port + '\/finance\/icbc\/sucss' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    #################################支付宝回调URL(财务系统IP（域名）及端口)#######################    #######print ssh.runcmd('sed -i \'s/xzxUrl\s*=.*/' + 'xzxUrl=http:\/\/' + wlan_ip + ':' + wlan_port + '\/html\/index.html' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    print ssh.runcmd('sed -i \'s/alipay_notify_url\s*=.*/' + 'alipay_notify_url=http:\/\/' + wlan_ip + ':' + finance_wlan_port + '\/finance\/alipay\/dispatch.action' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    #跳转支付宝支付界面URL(财务系统IP（域名）及端口)
    print ssh.runcmd('sed -i \'s/start_alipay_pay_url\s*=.*/' + 'start_alipay_pay_url=http:\/\/' + wlan_ip + ':' + finance_wlan_port + '\/finance\/alipay\/startAlipayPayment' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    ##################商城的地址###################
    print ssh.runcmd('sed -i \'s/hostNameShop\s*=.*/' + 'hostNameShop=http:\/\/' + hostname + ':' + idas_port +'\/'+ '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    #######print ssh.runcmd('sed -i \'s/pay_url\s*=.*/' + 'pay_url=http:\/\/' + wlan_ip + ':' + wlan_port + '\/idas\/icbc\/submittran' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    #微信支付HTTP证书在服务器中的路径，用来加载证书用
    print ssh.runcmd('sed -i \'s/wxpay_cert_file\s*=.*/' + 'wxpay_cert_file=\/usr\/local\/finance\/webapps\/finance\/WEB-INF\/classes\/wx\/apiclient_cert.p12' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    #微信回调URL(财务系统IP（域名）及端口)
    print ssh.runcmd('sed -i \'s/wxpay_callback_url\s*=.*/' + 'wxpay_callback_url=http:\/\/' + wlan_ip + ':' + finance_wlan_port + '\/finance\/wxpay\/wxpayCallBack' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    #银联支付回调URL(财务系统IP（域名）及端口)
    print ssh.runcmd('sed -i \'s/unionpay_callback_url\s*=.*/' + 'unionpay_callback_url=http:\/\/' + wlan_ip + ':' + finance_wlan_port + '\/finance' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    #跳转银联支付界面URL(财务系统IP（域名）及端口)
    print ssh.runcmd('sed -i \'s/start_union_pay_url\s*=.*/' + 'start_union_pay_url=http:\/\/' + wlan_ip + ':' + finance_wlan_port + '\/finance\/unionpay\/uniobpayRequest' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    #跳转农行支付界面URL
    print ssh.runcmd('sed -i \'s/start_abc_pay_url\s*=.*/' + 'start_abc_pay_url=http:\/\/' + hostname + ':' + finance_port + '\/finance\/abc\/startMerchantPayment' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    #跳转工行支付界面URL
    print ssh.runcmd('sed -i \'s/start_icbc_pay_url\s*=.*/' + 'start_icbc_pay_url=http:\/\/' + hostname + ':' + finance_port + '\/finance\/icbc\/submittran' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    #业务系统接口地址
    print ssh.runcmd('sed -i \'s/idas_url\s*=.*/' + 'idas_url=http:\/\/' + hostname + ':' + idas_port + '\/idas\/dispatch\/dispatch.action' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    print ssh.runcmd('sed -i \'s/file_url\s*=.*/' + 'file_url=\/usr\/local\/finance\/logs'+'\/' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    ##print ssh.runcmd('sed -i \'s/accessUrl=.*/' + 'accessUrl=http\\:\/\/' + hostname + '\\:' + idas_port + '\/' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    ##print ssh.runcmd('sed -i \'s/storageUrl=.*/' + 'storageUrl=\/usr\/local\/tomcat\/webapps' + '\/' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    #网上支付平台证书TrustPay.cer存放路径，如D:\WORK\cert\TrustPay.cer
    print ssh.runcmd('sed -i \'s/TrustPayCertFile=.*/' + 'TrustPayCertFile=' + '\/usr\/local\/finance\/webapps\/finance\/WEB-INF\/classes\/abc\/TrustPay.cer' + '/g\'' + ' ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
    #农行根证书文件abc.truststore存放路径，例如D:\WORK\cert\abc.truststore
    print ssh.runcmd('sed -i \'s/TrustStoreFile=.*/' + 'TrustStoreFile=' + '\/usr\/local\/finance\/webapps\/finance\/WEB-INF\/classes\/abc\/abc.truststore' + '/g\'' + ' ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
    #商户证书储存目录档名（当KeyStoreType=0时，必须设定）。指pfx证书，商户根据存放位置自行配置。如D:\WORK\cert\merchant.pfx
    print ssh.runcmd('sed -i \'s/MerchantCertFile=.*/' + 'MerchantCertFile=' + '\/usr\/local\/finance\/webapps\/finance\/WEB-INF\/classes\/abc\/abcpay.pfx' + '/g\'' + ' ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
    print ssh.runcmd('sed -i \'s/MerchantErrorURL=.*/' + 'MerchantErrorURL=http:\/\/' + hostname + ':' + finance_port + '\/finance\/abc\/ErrorPageInternal.jsp' + '/g\'' + ' ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
    #通知URL地址（农行回调URL地址），前面换成域名http://www.domain:端口/finance/abc/MerchantResult
    print ssh.runcmd('sed -i \'s/ResultNotifyURL\s*=.*/' + 'ResultNotifyURL=http:\/\/' + wlan_ip + ':' + finance_wlan_port + '\/finance\/abc\/MerchantResult' + '/g\'' + ' ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
    #工商银行-商户证书公钥
    print ssh.runcmd('sed -i \'s/ICBCCRT=.*/' + 'ICBCCRT=' + '\/usr\/local\/finance\/webapps\/finance\/WEB-INF\/classes\/icbc\/icbc.cer' + '/g\'' + ' ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
    #工商银行-商户证书私钥
    print ssh.runcmd('sed -i \'s/ICBCKEY=.*/' + 'ICBCKEY=' +  '\/usr\/local\/finance\/webapps\/finance\/WEB-INF\/classes\/icbc\/icbc.key' + '/g\'' + ' ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
    #交易日志文件存放目录。如D:/WORK/log
    print ssh.runcmd('sed -i \'s/LogPath=.*/' + 'LogPath=' + '\/usr\/local\/finance\/log' + '/g\'' + ' ' + app_config_path + '/' + app_config_file2).decode('UTF-8')


#start tomcat 
print ssh.runcmd('/usr/local/finance/bin/startup.sh').decode('UTF-8')

if not wlan_ip:
        print "cann't get wlan ip automatically, please get it manually"







