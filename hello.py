import platform
import json
import sqlite3
import pymysql
import json

name = 'wang peizhong'
FName = name.title()

wpz = {
    'firstName': 'peizhong',
    'lastName': 'wang',
    'age': 16,
    'ageStr': '16'
}

js = json.dumps(wpz)


def make_pizza(size, *toppings):
    "任意数量的实参"
    print('hello '+size)
    for top in toppings:
        print('- '+top)


def build_profile(name, **info):
    "任意数量的键值对"
    profile = {}
    profile['name'] = name
    for key, value in info.items():
        profile[key] = value
    return profile


make_pizza('nmii', 'aa', 'aa', 'aa')

wpz = build_profile(name='wang peizhong', age=27, sex='male')
print(wpz)


class ClassifyVO():
    def __init__(self, id, name="", fullName=""):
        self.Id = id
        self.Name = name
        self.FullName = fullName


class FunctionLocationVO():
    "dm_function_location"

    def __init__(self, name, classifyId, parentId):
        "构造函数"
        self.FlName = name
        self.ClassifyId = classifyId
        self.ParentId = parentId
        self.ClassifyProperty = ClassifyVO(classifyId)

    def Copy(self):
        print("copy self " + self.FlName)

    def GetObjectType(self):
        return 1


class SubStationFunctionLocationVO(FunctionLocationVO):
    def __init__(self):
        # super: 父类(超类)和子类关联
        super().__init__("SubStation", "2", "")

    def GetObjectType(self):
        return 2


fl1 = FunctionLocationVO("共同", "15048", 1)
fl1.Copy()
fl2 = SubStationFunctionLocationVO()
c = fl2.ClassifyProperty


actage = int(wpz['ageStr'])
count = 0
while True:
    city = input('which city do you live?')
    if(city == 'beijing'):
        continue
    count += 1
    if(city == 'shenzhen'):
        print('same, woo')
        break


for key, value in wpz.items():
    if (str(key).lower() == 'firstname'):
        print('first name is ' + value)
    elif (str(key).lower() == 'lastname'):
        print('last name is '+value)
aliens = []

prompt = "If you tell us who you are, we can personalize the messages you see."
prompt += "\nWhat is your first name? "
name = input(prompt)
print("\nHello, " + name + "!")

for num in range(30):
    newa = {'name': 'miomi', 'id': num, 'nini': str(num)}
    aliens.append(newa)

for a in aliens[0:3]:
    if (a['id'] % 2 == 1):
        a['name'] = 'odd'
    else:
        a['name'] = 'eve'

for k in sorted(wpz.keys()):
    print(k)

for v in wpz.values():
    print(v)

animal = ['cat', 'mouse', 'pig', 'dog']
animal.remove('cat')

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


def yourname(firstName, lastName, middleName=''):
    print(firstName+' '+lastName)
    return (firstName+' '+lastName).title()


yourname(lastName='wang', firstName='wang')


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
# functionLocations = [{'id': r[0], 'flName':r[2]} for r in cursor]
# print(json.dumps(functionLocations, ensure_ascii=False, indent=2))


sql3Conn.close()
mysqlConn.close()
print('Operation done successfully')


feed = feedparser.parse(
    'https://www.howstuffworks.com/podcasts/stuff-you-should-know.rss')
# feed = feedparser.parse('http://www.ifanr.com/feed')


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
