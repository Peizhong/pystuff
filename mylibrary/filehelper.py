import os
import platform


def getWorkspace():
    curOs = platform.system()
    print('current os is '+curOs)
    curRealse = platform.release()
    print('current release is '+curRealse)
    if curOs == "Darwin":
        downloadpath = r'/Users/Peizhong/Downloads'
    elif curOs == "Linux":
        downloadpath = r'/home/peizhong/downloads'
    else:
        downloadpath = r'E:/Downloads'
    return downloadpath


def getFileServer():
    curOs = platform.system()
    print('current os is '+curOs)
    curRealse = platform.release()
    print('current release is '+curRealse)
    if curOs == "Darwin":
        downloadpath = r'http://192.168.3.172/downloads/'
    elif curOs == "Linux":
        downloadpath = r'http://193.112.41.28/downloads/'
    else:
        downloadpath = r'localhost'
    return downloadpath


def findAllFile():
    localpath = getWorkspace()
    supportedFormat = ('.pdf', '.mkv', 'mp3', '.mp4', '.avi')
    selectedFiles = []
    for root, dirs, files in os.walk(localpath):
        for name in files:
            ext = os.path.splitext(name)
            if len(ext) > 1 and ext[1] in supportedFormat:
                selectedFiles.append(name)
    return selectedFiles
