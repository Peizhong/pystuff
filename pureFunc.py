
def getFormatedName(*names):
    fullName = ""
    for n in names:
        fullName += n
        fullName += " "
    return fullName[:-1].title()
