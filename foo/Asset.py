from Base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from BasicInfo import BasicInfo, TechparamInfo


class FlAssetConfig(Base):
    __tablename__ = 'DM_FL_ASSET'
    Id = Column('ID', String, primary_key=True)
    WorkspaceId = Column('WORKSPACE_ID', String)
    FunctionLocationId = Column('FUNCTION_LOCATION_ID', String)
    AssetId = Column('ASSET_ID', String)
    ObjectType = Column('OBJECT_TYPE', Integer)


class DeviceVO(Base):
    __tablename__ = 'DM_DEVICE'
    Id = Column('ID', String, primary_key=True)
    WorkspaceId = Column('WORKSPACE_ID', String, primary_key=True)
    DeviceName = Column('DEVICE_NAME', String)
    ClassifyId = Column('CLASSIFY_ID', String)
    AssetState = Column('ASSET_STATE', Integer)
    VoltageId = Column('BASE_VOLTAGE_ID', String)

    def __repr__(self):
        return '%r_%r' % (self.Id, self.DeviceName)


class FunctionLocationVO(Base):
    __tablename__ = 'DM_FUNCTION_LOCATION'
    Id = Column('ID', String, primary_key=True)
    WorkspaceId = Column('WORKSPACE_ID', String, primary_key=True)
    ParentId = Column('PARENT_ID', String)
    FlName = Column('FL_NAME', String)
    ClassifyId = Column('CLASSIFY_ID', String)
    SortNo = Column('SORT_NO', Integer)
    RunningState = Column('RUNNING_STATE', Integer)
    VoltageId = Column('BASE_VOLTAGE_ID', String)
    UpdateTime = Column('UPDATE_TIME', DateTime)
    FlAsset = relationship('FlAssetConfig', uselist=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ['ID', 'WORKSPACE_ID'],
            ['DM_FL_ASSET.FUNCTION_LOCATION_ID', 'DM_FL_ASSET.WORKSPACE_ID']
        ),
    )

    def __repr__(self):
        return '%r_%r' % (self.Id, self.FlName)
