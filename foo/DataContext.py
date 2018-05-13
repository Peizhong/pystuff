from sqlalchemy import *
from sqlalchemy.orm import *
from BillInfo import MainTransferVO
from BasicInfo import ClassifyConfig
from Asset import FunctionLocationVO

engine = create_engine(
    'sqlite:////Users/Peizhong/Downloads/avmt.db', echo=True)
metaData = MetaData(engine)

Session = sessionmaker(bind=engine)
session = Session()


def MainTransfers():
    result = session.query(MainTransferVO).all()
    print('get %d MainTransfers' % len(result))
    return result


def FunctionLocations(workspaceIds):
    if len(workspaceIds) > 0:
        result = session.query(FunctionLocationVO).filter(
            FunctionLocationVO.WorkspaceId.in_(workspaceIds)).order_by(FunctionLocationVO.SortNo).all()
    else:
        result = []
    print('get %d FunctionLocations' % len(result))
    return result


def ClassifyDict():
    result = {classify.Id: classify for classify in session.query(
        ClassifyConfig).filter(ClassifyConfig.IsShow == 1).order_by(ClassifyConfig.SortNo)}
    print('get %d ClassifyDict' % len(result.items()))
    return result
