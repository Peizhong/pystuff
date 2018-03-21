import platform
from flask import Flask
import json
import sqlite3
import pymysql
import feedparser
import requests
import urllib.request

app = Flask(__name__)

curOs = platform.system()
print('current os is '+curOs)
curRealse = platform.release()
print('current release is '+curRealse)
if curOs == "Darwin":
    sql3path = '/Users/Peizhong/Downloads/avmt.db'
else:
    sql3path = 'D:/Source/Repos/Comtop/Comtop.YTH/Comtop.YTH.App/bin/Debug/DB/avmt.db'

sql3Conn = sqlite3.connect(sql3path)
sql3Cur = sql3Conn.cursor()
print("Opened sqlite database successfully")

mysqlConn = pymysql.connect('193.112.41.28', 'root', 'mypass', 'MYDEV')
mysqlCur = mysqlConn.cursor()
print("Opened mariadb database successfully")


def tupleToString(t):
    if(len(t) < 1):
        return '()'
    res = ''
    for i in t:
        if i == None:
            res += 'null, '
        else:
            res += "'%s', " % str(i).replace('\\', '/')
    return res[:-2]


table_toTrans = ('DM_FUNCTION_LOCATION', 'DM_DEVICE',
                 'DM_FL_ASSET', 'DM_CLASSIFY', 'DM_BASEINFO_CONFIG', 'DM_TECHPARAM')

for table in table_toTrans:
    sourceSQL = 'select * from %s' % table
    print('doing %s' % sourceSQL)
    cursor = sql3Cur.execute(sourceSQL)
    for row in cursor:
        replaceSQL = 'replace into %s VALUES(%s) ' % (table, tupleToString(
            row))
        mysqlCur.execute(replaceSQL)
    mysqlConn.commit()
    print('done table %s' % table)
#functionLocations = [{'id': r[0], 'flName':r[2]} for r in cursor]
#print(json.dumps(functionLocations, ensure_ascii=False, indent=2))


sql3Conn.close()
mysqlConn.close()
print('Operation done successfully')


feed = feedparser.parse(
    'https://www.howstuffworks.com/podcasts/stuff-you-should-know.rss')
#feed = feedparser.parse('http://www.ifanr.com/feed')


def get_real_url(url):
    rs = requests.get(url)
    if rs.status_code > 400:
        return 'error'
    return rs.url


def downloadFile(info):
    print("downloading with urllib")
    f = urllib.request.urlopen(info[1])
    data = f.read()
    with open("downloads/"+info[0]+".mp3", "wb") as code:
        code.write(data)
    return 'okay'


if len(feed.entries) > 0:
    # 转换为元组
    feedList = [(e.title, e.link) for e in feed.entries]
    # 字典
    feedDict = [{f.title: f.link} for f in feed.entries]

    for f in feedList:
        al = downloadFile(f)
        break

print('hello, here is what i got')
