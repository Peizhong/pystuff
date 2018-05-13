#根据已有台账结构，自动创建参数
from Model.Asset import FunctionLocationVO,DeviceVO

def hello():
    f1= FunctionLocationVO('1','2','3','4','5')
    print(f1)

hello()