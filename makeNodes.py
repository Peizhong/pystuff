import sqlite3

DB_PATH = r'D:\Source\Repos\Comtop\Comtop.YTH\Comtop.YTH.App\bin\Debug\DB\avmt.db'

conn = sqlite3.connect(DB_PATH)

cursor = conn.execute('select * from dm_function_location')
"""
count = 0
for func in cursor.fetchall():
    cpFunc = list(func)
    for x in 'xyz':
        cpFunc[0] = cpFunc[0][:-1]+x
        cpFunc[2] = cpFunc[2][:-1]+x
        tpFunc = tuple(cpFunc)
        sql = "replace into dm_function_location values%s" % str(tpFunc)
        invalid_characaters = 'None,'
        sql = sql.replace(invalid_characaters, 'null,')
        conn.execute(sql)
        count += 1
print(count)
conn.commit()
cursor = conn.execute('select * from dm_device')
count = 0
for dev in cursor.fetchall():
    cpDev = list(dev)
    for x in 'abcdefghijk':
        cpDev[0] = cpDev[0][:-1]+x
        tpDev = tuple(cpDev)
        sql = "replace into dm_device values%s" % str(tpDev)
        invalid_characaters = 'None'
        sql = sql.replace(invalid_characaters, 'null')
        conn.execute(sql)
        count += 1

conn.commit()
"""

cursor = conn.execute('select * from dm_fl_asset')
count = 0
for fla in cursor.fetchall():
    cpFla = list(fla)
    for x in 'abcdefg':
        cpFla[0] = cpFla[0]+x
        cpFla[2] = cpFla[2][:-1]+x
        cpFla[3] = cpFla[3][:-1]+x
        tpFla = tuple(cpFla)
        sql = "replace into dm_fl_asset values%s" % str(tpFla)
        invalid_characaters = 'None'
        sql = sql.replace(invalid_characaters, 'null')
        conn.execute(sql)
        count += 1

conn.commit()

conn.close()
