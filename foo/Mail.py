import smtplib
from email.mime.text import MIMEText
from email.header import Header
import logging

from urllib import parse
from mytoolkit import queryConfig, findAllDownloadFile

logger = logging.getLogger(__name__)

mail_host = 'smtp.qq.com'
mail_user = queryConfig('emailaccount')
mail_pass = queryConfig('emailpasswd')

receivers = ['w.xy.z@live.com']


def sendMail(subject, message=''):
    message = MIMEText(message, 'plain', 'utf-8')
    message['From'] = Header("王培仲_python", 'utf-8')
    message['To'] = Header("QQ", 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(mail_user, receivers, message.as_string())
        logger.warning('邮件发送成功')
        smtpObj.quit()
        return True
    except smtplib.SMTPException:
        logger.error('无法发送邮件')
        smtpObj.quit()
        return False


def sendNewFile(filepath):
    '''下载到新文件后，邮件通知'''
    for f in findAllDownloadFile().values():
        if f.FullPath == filepath:
            msg = 'http://'+parse.quote(f.UrlPath)
            if sendMail(f.Name, msg):
                return True
    return False
