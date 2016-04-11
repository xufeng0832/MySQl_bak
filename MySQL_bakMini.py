#!/usr/bin/env python
#coding=utf-8
#__author__ = 'xuchao'
import time
import os
import smtplib
from email.mime.text import MIMEText
# 解决编码错误
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# 执行shell查看命令是否成功
def DDDD(cmd):
    os.system(cmd)
    Number1 = os.system('a=$?')
    if Number1 == 0:
        return u'成功'
    return u'失败'
# 备份时间
Back_file = time.strftime('%Y-%m-%d')+'_all.sql'
# 备份地址
Back_dir='/bak/'

mount = DDDD('mount -a')
# 注意修改密码
compress = DDDD('mysqldump -uroot -ppassword -h 192.168.0.175 --all-databases > %s%s'% (Back_dir,Back_file))
Clear = DDDD('find %s -mtime +7 -exec rm -rf {} \;' %Back_dir)
time.sleep(10)
umount = DDDD('umount /bak')
sleep = DDDD('hdparm -Y /dev/sdd')
# 邮件服务地址
HOST = 'xxxx.xxx.com'                              #定义stmp主机
SUBJECT = '175 Mysql数据库备份'                   #定义邮件主题
TO = 'chao.xu@xxxx.com'                         #定义收件人
FROM = 'chao.xu@xxxx.com'                   #定义发件人
msg = MIMEText('''
    <table width="800" border="0" cellspacing="0" cellpadding="4">
        <tr>
            <td bgcolor="#EFEBDE" height="100" style="font-size:13px">
            1)挂载:%s<br>
            2)备份:%s<br>
            3)清理:%s<br>
            4)卸载:%s<br>
            5)睡眠:%s<br>
            </td>
        </tr>
    </table>'''%(mount,compress,Clear,umount,sleep),"html","utf-8")
msg['Subject'] = SUBJECT
msg['From'] = FROM
msg['To'] = TO
try:
    server = smtplib.SMTP()         #建立一个SMTP()对象
    server.connect(HOST,"25")
    server.starttls()               #启动安全传输模式
    server.login("xxxx","xxxx")    #邮箱账号登陆校验
    server.sendmail(FROM,TO,msg.as_string())                #邮件发送
    server.quit()           #断开SMTP连接
    print(u'邮件发送成功')
except Exception, e:
    print('失败:'+str(e))