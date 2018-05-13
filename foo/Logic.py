from Asset import FunctionLocationVO


def getFullPath(node, route):
    route.append(node.Name)
    if not node.ParentNode:
        return route
    return getFullPath(node.ParentNode, route)


class Node(object):

    def __init__(self, functionlocation):
        if isinstance(functionlocation, FunctionLocationVO):
            self.FunctionLocation = functionlocation
        else:
            self.FunctionLocation = None
        self.ParentNode = None
        self.Nodes = []

    @property
    def Name(self):
        if self.FunctionLocation:
            return self.FunctionLocation.FlName
        return None

    @property
    def FullPath(self):
        toroot = getFullPath(self, [])
        fullpath = r'/'.join(reversed(toroot))
        return fullpath
