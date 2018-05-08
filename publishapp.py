import os
import shutil
import sys
import re
import codecs
import sqlite3
import xml.etree.ElementTree as ET

solutionPath = r''
projectPath = r'D:\Source\Repos\Comtop\Comtop.YTH\Comtop.YTH.App'
buildPath = r'D:\Source\Repos\Comtop\Comtop.YTH\Comtop.YTH.App\bin\Release'


def get_desktop():
    return os.path.join(os.path.expanduser("~"), 'Desktop')


def lastestFramework():
    rootdir = 'C:/Windows/Microsoft.NET/Framework'
    for root, dirs, files in os.walk(rootdir):
        for name in sorted(dirs, reverse=True):
            fullpath = os.path.join(rootdir, name, 'MSBuild.exe')
            if os.path.exists(fullpath):
                return fullpath
    print('no framework found')
    sys.exit()


def buildProject():
    print("now building project...")
    devenv = r'"C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/Common7/IDE/devenv.com"'
    cmd = r'%s D:/Source/Repos/Comtop/Comtop.YTH.sln /rebuild "Release" /Project Comtop.YTH.App' % (
        devenv)
    p = os.popen(cmd)
    res = p.read()
    if "0 failed" in res:
        return True
    else:
        print(res)
        sys.exit()


def getReleaseFolder(version):
    desktopPath = get_desktop()
    lastestZip = ''
    for root, dirs, files in os.walk(desktopPath):
        # 找到最新的压缩包(按名字排序)
        for name in sorted(files, reverse=True):
            if(name.startswith('建模工具') and os.path.splitext(name)[1] == '.zip'):
                lastestZip = name
                print('latest zip is %s' % (os.path.join(root, lastestZip)))
                break
    if not lastestZip:
        print('没有找到压缩包')
        sys.exit()
    # 准备打包的文件夹
    newName = '建模工具 %s' % (version)
    newFolderPath = os.path.join(desktopPath, newName)
    if os.path.exists(newFolderPath):
        print('删除现有文件夹%s' % (newFolderPath))
        shutil.rmtree(newFolderPath)
    shutil.unpack_archive(os.path.join(desktopPath, lastestZip), newFolderPath)
    for root, dirs, files in os.walk(newFolderPath):
        for name in dirs:
            try:
                os.rename(os.path.join(root, name),
                          os.path.join(root, newName))
            except Exception as e:
                print(e)
            break
        break
    return {
        'zip': os.path.join(root, lastestZip),
        'folder': newFolderPath,
        'workFolder': os.path.join(newFolderPath, newName)
    }


def getCopyFileList(configPath):
    files = []
    tree = ET.parse(configPath)
    root = tree.getroot()
    for child in root:
        if(child.tag == 'UpdateFileList'):
            for file in child:
                files.append(file.text)
            break
    return files


def copyBuildFile(releasePath):
    configPath = os.path.join(buildPath, 'UpdateConfigV2.xml')
    dbSrcipts = {
        'db': '',
        'sql': []
    }
    for name in getCopyFileList(configPath):
        ext = os.path.splitext(name)[1]
        if ext in ['.dll', '.xml', '.exe', '.config']:
            src = os.path.join(buildPath, name)
            if os.path.exists(src):
                dst = os.path.join(releasePath, name)
                shutil.copyfile(src, dst)
            else:
                print("not found "+src)
        elif ext == '.db':
            dbSrcipts['db'] = name
        elif ext == '.txt':
            dbSrcipts['sql'].append(name)
    # 处理数据库和脚本
    releaseDbPath = os.path.join(releasePath, 'DB')
    if os.path.exists(releaseDbPath):
        shutil.rmtree(releaseDbPath)
    os.makedirs(releaseDbPath)
    projectDbPath = os.path.join(projectPath, 'DB')
    databaseFile = os.path.join(projectPath, dbSrcipts['db'])
    releaseDatabaseFile = os.path.join(releasePath, dbSrcipts['db'])
    shutil.copyfile(databaseFile, releaseDatabaseFile)
    conn = sqlite3.connect(releaseDatabaseFile)
    sqlVer = re.compile(r'\d{1,2}\.\d{2}')
    for sql in dbSrcipts['sql']:
        targetVersion = sqlVer.search(sql).group()
        for root, dirs, files in os.walk(projectDbPath):
            for d in dirs:
                sourceVersion = sqlVer.search(d).group()
                if targetVersion == sourceVersion:
                    targetPath = os.path.join(releaseDbPath, targetVersion)
                    # os.makedirs(targetPath)
                    # 拷贝project下的dbscript文件夹到release
                    shutil.copytree(os.path.join(projectDbPath, d), targetPath)
            break
    for root, dirs, files in os.walk(releaseDbPath):
        for name in files:
            if os.path.splitext(name)[1] == '.txt':
                with open(os.path.join(root, name), encoding='utf-8-sig') as sqlfile:
                    u = sqlfile.read()
                    conn.executescript(u)
    conn.commit()
    # clean backup table
    cursor = conn.execute(
        r"SELECT name FROM sqlite_master where type = 'table' and name like 'BK20%'")
    for row in cursor.fetchall():
        conn.execute('drop table %r' % row[0])
    conn.execute('vacuum')
    conn.execute('analyze')
    conn.close()


def packFile(packName, rootPath):
    try:
        shutil.make_archive(packName, 'zip', rootPath)
        shutil.rmtree(rootPath)
        print('complete: %s.zip' % (os.path.join(rootPath, packName)))
    except Exception as e:
        print(e)
        sys.exit()


def _main():
    if len(sys.argv) > 1:
        publicVersion = '(%s)' % sys.argv[1]
    else:
        publicVersion = '(%s)' % input('input the publish version: ')
    cmd = buildProject()
    releaseInfo = getReleaseFolder(publicVersion)
    copyBuildFile(releaseInfo['workFolder'])
    packFile(releaseInfo['folder'], releaseInfo['folder'])


if __name__ == '__main__':
    _main()
