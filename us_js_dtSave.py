#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import datetime
import pymysql
import pandas as pd

from sqlalchemy import create_engine
import pymysql
import pandas as pd
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication 
import datetime




engine_us = create_engine('mysql+pymysql://root:123456@localhost:3306/SP500_Nas100')
engine_js = create_engine('mysql+pymysql://root:123456@localhost:3306/JS225_JS400')
# 查询语句，选出employee表中的所有数据 "JS225_JS400"
sql_sp500 = 'select * from sp500_s  ; '

sql_nas100 = 'select * from nasdap100_s  ; '


sql_j225 = 'select * from js225_s  ; '
sql_j400 = 'select * from js400_s  ; '

ln = os.getcwd()






def savedt():


    df_sp500 = pd.read_sql_query(sql_sp500, engine_us)
    df_nas100 = pd.read_sql_query(sql_nas100, engine_us)
    df_js225 = pd.read_sql_query(sql_j225, engine_js)
    df_js400 =pd.read_sql_query(sql_j400, engine_js)


    
    excelFile1 = '{0}/{1}.xlsx'.format(ln,"df_sp500") # 处理了文件属于当前目录下！
    excelFile2 = '{0}/{1}.xlsx'.format(ln,"df_nas100") # 处理了文件属于当前目录下！
    excelFile3 = '{0}/{1}.xlsx'.format(ln,"df_js225") # 处理了文件属于当前目录下！
    excelFile4 = '{0}/{1}.xlsx'.format(ln,"df_js400") # 处理了文件属于当前目录下！


    df_sp500.to_excel(excelFile1)
    df_nas100.to_excel(excelFile2)
    df_js225.to_excel(excelFile3)
    df_js400.to_excel(excelFile4)


 
def sendmail():



  


      #发送邮件参数设置   
    sender = '291109028@qq.com'#发送者邮箱
    password = 'fymphheytkutbibe'#发送者邮箱授权码
    smtp_ip='smtp.qq.com'#smtp服务器ip,根据发送者邮箱而定
    receiver = ['291109028@qq.com']#接收者邮箱 
    title='us_js指数成分股'#邮件主题
    content = 'hello,4个指数成分股跑起来的情况'#邮件内容
    annex_path=ln#报表存储路径，也是附件路径




    try:
        
        #传入邮件发送者、接受者、抄送者邮箱以及主题    
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = ','.join(receiver)
        message['Subject'] = Header(str(datetime.datetime.now().date())+title, 'utf-8')
        
        #添加邮件内容
        text_content = MIMEText(content)
        message.attach(text_content)
        
        #添加附件    


               # 首先是xlsx类型的附件
        xlsxpart1 = MIMEApplication(open('{0}/df_js225.xlsx'.format(ln), 'rb').read())
        xlsxpart1.add_header('Content-Disposition', 'attachment', filename='df_js225.xlsx')
        xlsxpart2 = MIMEApplication(open('{0}/df_js400.xlsx'.format(ln), 'rb').read())
        xlsxpart2.add_header('Content-Disposition', 'attachment', filename='df_js400.xlsx')
        xlsxpart3 = MIMEApplication(open('{0}/df_nas100.xlsx'.format(ln), 'rb').read())
        xlsxpart3.add_header('Content-Disposition', 'attachment', filename='df_nas100.xlsx')
        xlsxpart4 = MIMEApplication(open('{0}/df_sp500.xlsx'.format(ln), 'rb').read())
        xlsxpart4.add_header('Content-Disposition', 'attachment', filename='df_sp500.xlsx')

        message.attach(xlsxpart1)
        message.attach(xlsxpart2)
        message.attach(xlsxpart3)
        message.attach(xlsxpart4)

        
        #登入邮箱发送报表
        server = smtplib.SMTP(smtp_ip)#端口默认是25,所以不用指定
        server.login(sender,password)
        server.sendmail(sender, receiver, message.as_string())
        server.quit()
        print('success!',datetime.datetime.now())
        
    except smtplib.SMTPException as e:
        print('error:',e,datetime.datetime.now()) #打印错误




if __name__ == '__main__':
    savedt()
    sendmail()

# 0 19 1 * *  /usr/local/bin/python3.6 /root/us_js_dtSave.py
# 每个月的1号的19点钟运行xxx.sh
# 分钟、小时、日子可以更改，后两项为*就是monthly。
