from Logic import Node
from Asset import FunctionLocationVO
from DataContext import MainTransfers, FunctionLocations
from random import randint


AccountTreeDict = {}


def BuildTree():
    workspaces = []
    for bill in MainTransfers():
        if len(bill.Workspaces) > 0:
            workspaces = bill.Workspaces
            break
    for workspace in workspaces:
        workspaceDict = {
            func.Id: Node(func) for func in FunctionLocations([workspace.Id])}
        AccountTreeDict[workspace.Id] = workspaceDict
    for workspace, workspaceDict in AccountTreeDict.items():
        for node in workspaceDict.values():
            # find parent
            parent = node.FunctionLocation.ParentId
            if parent and parent in workspaceDict.keys():
                parentNode = workspaceDict[parent]
                parentNode.Nodes.append(node)
                node.ParentNode = parentNode
    root = []
    for workspace in workspaces:
        if workspace.Id in AccountTreeDict.keys():
            targetDict = AccountTreeDict[workspace.Id]
            if workspace.ObjectId in targetDict.keys():
                root.append(targetDict[workspace.ObjectId])
                keys = list(targetDict.keys())
                for _ in range(10):
                    randomNode = targetDict[keys[randint(0, len(keys))]]
                    print('random node: %s' % randomNode.FullPath)
    return root


BuildTree()
