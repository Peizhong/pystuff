from sqlalchemy import *
from sqlalchemy.orm import *
from BillInfo import MainTransferVO
from BasicInfo import ClassifyConfig, BaseinfoConfig, ColumnInfo
from Asset import FunctionLocationVO, DeviceVO

engine = create_engine(
    'sqlite:////Users/Peizhong/Downloads/avmt.db', echo=True)
metaData = MetaData(engine)

Session = sessionmaker(bind=engine)
session = Session()


def MainTransfers():
    result = session.query(MainTransferVO).all()
    print('get %d MainTransfers' % len(result))
    return result


classifyDict = {}


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


def QueryDeivce(functionlocation):
    if len(deivceDict.keys()) < 1:
        for d in session.query(DeviceVO):
            d.Techparams = QueryTechparam(d)
            deivceDict['%s_%s' % (d.Id, d.WorkspaceId)] = d
    key = '%s_%s' % (functionlocation.AssetId, functionlocation.WorkspaceId)
    if key in deivceDict.keys():
        return deivceDict[key]
    return None


def FillDeviceInfo(functionlocation):
    deivce = QueryDeivce(functionlocation)
    if deivce:
        # 基本信息&技术参数
        classify = QueryClassify(deivce.ClassifyId)
        functionlocation.AssetObject = deivce


def FillPartInfo(functionlocation):
    pass


def FillFunction(functionlocation):
    session
    if functionlocation.FlAsset:
        if functionlocation.FlType == 3:
            FillDeviceInfo(functionlocation)
        functionlocation.AssetObject = DeviceVO()
    else:
        classify = QueryClassify(functionlocation.ClassifyId)


def FunctionLocations(workspaceIds):
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
        if func.AssetId:
            if func.FlType == 3:
                func.AssetObject = QueryDeivce(func)
            else:
                pass
        else:
            pass
        result.append(func)
    print('get %d FunctionLocations' % len(result))
    return result
