import os
import shutil
import sys
import re
import xml.etree.ElementTree as ET

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
            if(name[:4] == '建模工具' and name[-4:] == '.zip'):
                lastestZip = name
                print('latest zip is %s' % (os.path.join(root, lastestZip)))
                break
        if len(lastestZip) < 1:
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
    for name in getCopyFileList(configPath):
        ext = os.path.splitext(name)[1]
        if ext in ['.dll', '.xml', '.exe', '.config']:
            src = os.path.join(buildPath, name)
            if os.path.exists(src):
                dst = os.path.join(releasePath, name)
                shutil.copyfile(src, dst)
            else:
                print("not found "+src)
        elif ext in ['.txt', '.db']:
            # 脚本：拷贝工程目录的db和脚本?? 名字不一样。。
            v = re.match('\d{1,2}\.\d{2}', name)
            src = os.path.join(projectPath, name)
            if os.path.exists(src):
                dst = os.path.join(releasePath, name)
                shutil.copyfile(src, dst)
            else:
                print("not found "+src)


def packFile(packName, rootPath):
    try:
        shutil.make_archive(packName, 'zip', rootPath)
        shutil.rmtree(rootPath)
        print('complete: %s.zip' % (os.path.join(rootPath, packName)))
    except Exception as e:
        print(e)
        sys.exit()


cmd = buildProject()

pubilcVersion = input('input the publish version: ')

releaseInfo = getReleaseFolder(pubilcVersion)

copyBuildFile(releaseInfo['workFolder'])

packFile(releaseInfo['folder'], releaseInfo['folder'])
