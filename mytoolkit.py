import os
import platform


def getDownloadPath():
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
