import os
import shutil
import sys
import xml.etree.ElementTree as ET


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
    return ''


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


def copyBuidFile(releasePath):
    buildPath = 'D:/Source/Repos/avmt/debug/'
    buildPath = 'C:/Users/wxyz/Source/avmt/Comtop.YTH//Comtop.YTH.App/bin/Release'
    configPath = os.path.join(buildPath, 'UpdateConfigV2.xml')
    for name in getCopyFileList(configPath):
        src = os.path.join(buildPath, name)
        if os.path.exists(src):
            dst = os.path.join(releasePath, name)
            shutil.copyfile(src, dst)
        else:
            print("not found "+src)


def packFile(packName, rootPath):
    shutil.make_archive(packName, 'zip', rootPath)
    shutil.rmtree(rootPath)


pubilcVersion = input('input the publish version: ')

releaseInfo = getReleaseFolder(pubilcVersion)

copyBuidFile(releaseInfo['workFolder'])

packFile(releaseInfo['folder'], releaseInfo['folder'])

framepath = lastestFramework()
p = os.popen('%s /ver' % (framepath))

print(p.read())
