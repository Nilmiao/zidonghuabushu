# -*- coding: utf-8 -*-
# deploy app system automatically
from pyssh import PySSH
import os
import sys
import paramiko
import re

# set app package path
app_path = r'E:\test\idas.war'

# set the basic remote server info
hostname = '192.168.3.23'
username = 'root'
passwd = '123456'
idas_port = '8080'
wlan_port = '9020'
finance_port='8090'
wlan_finance_port='9120'
tomcat_path = '/usr/local/tomcat'
app_name = 'idas'
app_back_path = '/usr/local/projectback/idas'
app_server_path = tomcat_path + '/webapps/' + app_name
app_config_path = app_server_path + '/WEB-INF/classes'
app_config_file1 = 'projectUrl.properties'
app_config_file2 = 'TrustMerchant.properties'
app_config_file3 = 'oracle_db.properties'
app_config_file4 = 'quartz-job-launcher-context.xml'


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

# unzip the app package
#print ssh.runcmd('unzip ' + tomcat_path + '/webapps/' + app_name + '.war' + ' -d ' + tomcat_path + '/webapps/' + app_name)
print ssh.runcmd('unzip ' + app_server_path + '.war' + ' -d ' + app_server_path)

# copy the backup config files to the app path
print ssh.runcmd('rm -rf ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
print ssh.runcmd('rm -rf ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
print ssh.runcmd('rm -rf ' + app_config_path + '/' + app_config_file3).decode('UTF-8')
print ssh.runcmd('rm -rf ' + app_config_path + '\/spring\/' + app_config_file4).decode('UTF-8')
print ssh.runcmd('cp ' + app_back_path + '/' + app_config_file1 + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
print ssh.runcmd('cp ' + app_back_path + '/' + app_config_file2 + ' ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
print ssh.runcmd('cp ' + app_back_path + '/' + app_config_file3 + ' ' + app_config_path + '/' + app_config_file3).decode('UTF-8')
print ssh.runcmd('cp ' + app_back_path + '/' + app_config_file4 + ' ' + app_config_path + '\/spring\/' + app_config_file4).decode('UTF-8')



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
    print ssh.runcmd('sed -i \'s/accessUrl=.*/' + 'accessUrl=http\\:\/\/' + hostname + '\\:' + idas_port + '\/' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    print ssh.runcmd('sed -i \'s/storageUrl=.*/' + 'storageUrl=\/usr\/local\/tomcat\/webapps\/' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    ####### 品牌的 ###############
    print ssh.runcmd('sed -i \'s/brandUrl=.*/' + 'brandUrl=http:\/\/' + hostname + ':' + idas_port + '\/utopMall\/wap\/brand\/more?brandId=' + '\/' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    ####### 商品的 ##############
    print ssh.runcmd('sed -i \'s/goodsUrl=.*/' + 'goodsUrl=http:\/\/' + hostname + ':' + idas_port + '\/utopMall\/wap\/goods\/goodsDetail?goodsId=' + '\/' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    ######### 店铺 ##############
    print ssh.runcmd('sed -i \'s/shopUrl=.*/' + 'shopUrl=http:\/\/' + hostname + ':' + idas_port + '\/utopMall\/wap\/shop\/shopInfo?flag=true&shopId=' + '\/' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    ######################分享图集地址##############
    print ssh.runcmd('sed -i \'s/share_collective_url\s*=.*/' + 'share_collective_url=http:\/\/' + hostname + ':' + idas_port + '\/idas\/share\/collectiveDraving?collectiveDravingId=' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    ######################分享效果图地址##############
    print ssh.runcmd('sed -i \'s/share_rendering_url\s*=.*/' + 'share_rendering_url=http:\/\/' + hostname + ':' + idas_port + '\/idas\/share\/rendering?renderingId=' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    #######################农行支付请求url#################
    print ssh.runcmd('sed -i \'s/abc_pay_url\s*=.*/' + 'abc_pay_url=http:\/\/' + wlan_ip + ':' + wlan_port + '\/idas\/abc\/MerchantPayment' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    #######################工行支付请求url#################
    print ssh.runcmd('sed -i \'s/icbc_pay_url\s*=.*/' + 'icbc_pay_url=http:\/\/' + wlan_ip + ':' + wlan_port + '\/idas\/icbc\/submittran' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    #####################工行支付回调IP########################
    print ssh.runcmd('sed -i \'s/icbc_pay_refund_url\s*=.*/' + 'icbc_pay_refund_url=http:\/\/' + wlan_ip + ':' + wlan_port + '\/idas\/icbc\/sucss' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    ##################小白的地址###################
    print ssh.runcmd('sed -i \'s/xzxUrl\s*=.*/' + 'xzxUrl=http:\/\/' + hostname + ':' + idas_port + '\/html\/index.html' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    ##################商城的地址###################
    print ssh.runcmd('sed -i \'s/hostNameShop\s*=.*/' + 'hostNameShop=http:\/\/' + hostname + ':' + idas_port  + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    ##################选择屋拓邦的十大理由###################
    print ssh.runcmd('sed -i \'s/lyUrl\s*=.*/' + 'lyUrl=http:\/\/' + hostname + ':' + idas_port + '\/html\/reason.html' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    ############################财务系统接口########################
    print ssh.runcmd('sed -i \'s/pay_url\s*=.*/' + 'pay_url=http:\/\/' + hostname + ':' + finance_port + '\/finance\/dispatch\/dispatch.action' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    ##########################财务系统支付成功回调业务系统的接口##############
    print ssh.runcmd('sed -i \'s/result_pay_url\s*=.*/' + 'result_pay_url=http:\/\/' + hostname + ':' + idas_port + '\/idas\/dispatch\/dispatch.action' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    ##########################财务系统支付宝支付成功回调财务系统的接口##############
    print ssh.runcmd('sed -i \'s/result_alipay_url\s*=.*/' + 'result_alipay_url=http:\/\/' + wlan_ip + ':' + wlan_finance_port + '\/finance\/alipay\/dispatch.action' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    #网上支付平台证书TrustPay.cer存放路径，如D:\WORK\cert\TrustPay.cer
    print ssh.runcmd('sed -i \'s/TrustPayCertFile=.*/' + 'TrustPayCertFile=' + app_server_path + '\/WEB-INF\/classes\/abc\/TrustPay.cer' + '/g\'' + ' ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
    #农行根证书文件abc.truststore存放路径，例如D:\WORK\cert\abc.truststore
    print ssh.runcmd('sed -i \'s/TrustStoreFile=.*/' + 'TrustStoreFile=' + app_server_path + '\/WEB-INF\/classes\/abc\/abc.truststore' + '/g\'' + ' ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
    #商户证书储存目录档名（当KeyStoreType=0时，必须设定）。指pfx证书，商户根据存放位置自行配置。如D:\WORK\cert\merchant.pfx
    print ssh.runcmd('sed -i \'s/MerchantCertFile=.*/' + 'MerchantCertFile=' + app_server_path + '\/WEB-INF\/classes\/abc\/abcpay.pfx' + '/g\'' + ' ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
    #通知URL地址（农行回调URL地址），前面换成域名http://www.domain:端口/finance/abc/MerchantResult
    print ssh.runcmd('sed -i \'s/ResultNotifyURL\s*=.*/' + 'ResultNotifyURL=http:\/\/' + hostname + ':' + finance_port + '\/finance\/abc\/MerchantResult' + '/g\'' + ' ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
    #工商银行-商户证书公钥
    print ssh.runcmd('sed -i \'s/ICBCCRT=.*/' + 'ICBCCRT=' + app_server_path + '\/WEB-INF\/classes\/icbc\/icbc.cer' + '/g\'' + ' ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
    #工商银行-商户证书私钥
    print ssh.runcmd('sed -i \'s/ICBCKEY=.*/' + 'ICBCKEY=' + app_server_path + '\/WEB-INF\/classes\/icbc\/icbc.key' + '/g\'' + ' ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
    #交易日志文件存放目录。如D:/WORK/log
    print ssh.runcmd('sed -i \'s/LogPath=.*/' + 'LogPath=' + tomcat_path + '\/log\/abclog' + '/g\'' + ' ' + app_config_path + '/' + app_config_file2).decode('UTF-8')
    #########################日记分享链接##################
    print ssh.runcmd('sed -i \'s/share_url=.*/' + 'share_url=http:\/\/' + hostname + ':' + idas_port + '\/idas\/wap\/diary\/share\?diaryId=' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    ##########################工程保障分享页面########################
    print ssh.runcmd('sed -i \'s/projectGtUrl=.*/' + 'projectGtUrl=http:\/\/'+ hostname + ':' + idas_port +'\/idas\/share\/gcbzUrl' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    ########################自定义推荐页面详情地址#######################
    print ssh.runcmd('sed -i \'s/indexRecommend_url=.*/' + 'indexRecommend_url=http:\/\/'+ hostname + ':' + idas_port +'\/idas\/recommend\/detail?hrId=' + '/g\'' + ' ' + app_config_path + '/' + app_config_file1).decode('UTF-8')
    ########################数据库配置#######################
    print ssh.runcmd('sed -i \'s/url=.*/' + 'url=jdbc\\\:oracle\\\:thin\\\:@192.168.3.23\\\:1521\:orcl'+ '/g\'' + ' ' + app_config_path + '/' + app_config_file3).decode('UTF-8')



# start tomcat 
print ssh.runcmd('/usr/local/tomcat/bin/startup.sh').decode('UTF-8')

if not wlan_ip:
    print "cann't get wlan ip automatically, please get it manually"







