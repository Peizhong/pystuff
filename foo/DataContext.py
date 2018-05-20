from sqlalchemy import *
from sqlalchemy.orm import *
import redis
import json
from collections import namedtuple
from foo.BillInfo import MainTransferVO
from foo.BasicInfo import ClassifyConfig, BaseinfoConfig, ColumnInfo
from foo.Asset import FunctionLocationVO, DeviceVO

from mytoolkit import queryConfig

jsonBaseinfo = namedtuple(
    'jsonBaseinfo', 'Id BaseinfoTypeid FiledColumn FieldName SortNo Dicts')
jsonBasedict = namedtuple('jsonBasedic', 'Name Value')

engine = create_engine('sqlite:///%s' % queryConfig('avmtdb'), echo=False)
metaData = MetaData(engine)

Session = sessionmaker(bind=engine)
session = Session()

pool = redis.ConnectionPool(host=queryConfig('host'), port='6379', db=0)


def MainTransfers():
    result = session.query(MainTransferVO).all()
    print('get %d MainTransfers' % len(result))
    return result


classifyDict = {}


def QueryBaseinfoConfig(baseinfoTypeId=''):
    result = []
    query = session.query(BaseinfoConfig).filter(
        BaseinfoConfig.IsDisplay == 1)
    if baseinfoTypeId:
        query = query.filter(BaseinfoConfig.BaseinfoTypeId == baseinfoTypeId)
    for bc in query:
        result.append(bc)
    print('QueryBaseinfoConfig %d' % len(result))
    print(result[1])
    return result


def SetBaseinfoBuffer():
    count = 0
    r = redis.Redis(connection_pool=pool)
    for vo in QueryBaseinfoConfig():
        d = None
        if vo.Dictonary:
            d = []
            for dt in vo.Dictonary:
                d.append(jsonBasedict(dt.DictKey, dt.DictValue)._asdict())
        dvo = jsonBaseinfo(vo.Id, vo.BaseinfoTypeId,
                           vo.ColumnName, vo.FieldName, vo.SortNo, d)._asdict()
        j = json.dumps(dvo, ensure_ascii=False)
        r.hset('baseinfoconfig', vo.Id, j)
        count += 1
    return count


def GetBaseinfoBuffer():
    r = redis.Redis(connection_pool=pool)
    count = 0
    for v in r.hvals('baseinfoconfig'):
        dvo = json.loads(v)
        print(dvo)
        count += 1
    return count


def QueryClassify(classifyId):
    if classifyId not in classifyDict.keys():
        classify = session.query(ClassifyConfig).filter(
            ClassifyConfig.Id == classifyId and ClassifyConfig.IsShow == 1).first()
        classifyDict[classifyId] = classify
    return classifyDict[classifyId]


def QueryTechparam(accountObject):
    classify = QueryClassify(accountObject.ClassifyId)
    if not classify or not classify.TechparamConfigs:
        return None
    columns = [tp.ColumnName for tp in classify.TechparamConfigs]
    paramToQuery = ','.join(columns)
    raw = 'select %s from %s where id=:oid and workspace_id=:wid' % (
        paramToQuery, classify.TableName)
    row = engine.execute(text(raw), oid=accountObject.Id,
                         wid=accountObject.WorkspaceId).fetchone()
    if not row:
        return None
    items = [ColumnInfo(col, row[col]) for col in columns]
    return items


deivceDict = {}


def QueryDeiceByWorkspace(workspaceIds):
    formatedId = ','.join(workspaceIds)
    sql = text(
        'select d.* from dm_fl_asset fla, dm_device d '
        'where fla.workspace_id in (:w) and '
        'fla.asset_id = d.id and '
        'fla.workspace_id = d.workspace_id')
    result = []
    for row in engine.execute(sql, w=formatedId).fetchall():
        d = DeviceVO()
        d.Id = row['ID']
        d.WorkspaceId = row['WORKSPACE_ID']
        d.DeviceName = row['DEVICE_NAME']
        d.ClassifyId = row['CLASSIFY_ID']
        d.AssetState = row['ASSET_STATE']
        d.VoltageId = row['BASE_VOLTAGE_ID']
        d.IsShareDevice = row['IS_SHARE_DEVICE']
        d.UpdateTime = row['UPDATE_TIME']
        d.Techparams = QueryTechparam(d)
        deivceDict['%s_%s' % (d.Id, d.WorkspaceId)] = d
    print('get %d devices' % len(deivceDict.keys()))


def QueryDeivce(functionlocation):
    key = '%s_%s' % (functionlocation.AssetId, functionlocation.WorkspaceId)
    if key in deivceDict.keys():
        return deivceDict[key]
    return None


def FillDeviceInfo(functionlocation):
    deivce = QueryDeivce(functionlocation)
    if deivce:
        # 基本信息&技术参数
        functionlocation.AssetObject = deivce


def FillPartInfo(functionlocation):
    pass


def FillFunction(functionlocation):
    if functionlocation.AssetId:
        if functionlocation.FlType == 3:
            FillDeviceInfo(functionlocation)
    else:
        functionlocation.Techparams = QueryTechparam(functionlocation)


def FunctionLocations(workspaceIds):
    QueryDeiceByWorkspace(workspaceIds)
    formatedId = ','.join(workspaceIds)
    sql = text(
        'select f.*, fla.asset_id from dm_function_location f left join dm_fl_asset fla '
        'on f.id = fla.function_location_id and f.workspace_id = fla.workspace_id '
        'where f.workspace_id in (:w)')
    result = []
    for row in engine.execute(sql, w=formatedId).fetchall():
        func = FunctionLocationVO()
        func.Id = row['ID']
        func.WorkspaceId = row['WORKSPACE_ID']
        func.ParentId = row['PARENT_ID']
        func.FlName = row['FL_NAME']
        func.ClassifyId = row['CLASSIFY_ID']
        func.FlType = row['FL_TYPE']
        func.SortNo = row['SORT_NO']
        func.RunningState = row['RUNNING_STATE']
        func.VoltageId = row['BASE_VOLTAGE_ID']
        func.UpdateTime = row['UPDATE_TIME']
        func.AssetId = row['ASSET_ID']
        FillFunction(func)
        result.append(func)
    print('get %d FunctionLocations' % len(result))
    return result
