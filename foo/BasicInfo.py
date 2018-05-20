from foo.Base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from collections import namedtuple

ColumnInfo = namedtuple('ColumnInfo', 'ColumnName Value')


class BaseinfoConfig(Base):
    __tablename__ = 'DM_BASEINFO_CONFIG'
    Id = Column(String, primary_key=True)
    BaseinfoTypeId = Column('BASEINFO_TYPEID', String,
                            ForeignKey('DM_CLASSIFY.BASEINFO_TYPEID'))
    FieldName = Column('FIELD_NAME', String)
    ColumnName = Column('FIELD_COLUMN', String)
    DictonaryId = Column('DICTIONARY_ID', Integer)
    Dictonary = relationship('BaseinfoDict')
    SortNo = Column('SORT_NO', Integer)
    IsDisplay = Column('IS_DISPLAY', Integer)

    def __repr__(self):
        return '%r_%r_%r' % (self.BaseinfoTypeId, self.ColumnName, self.FieldName)


class BaseinfoDict(Base):
    __tablename__ = 'DM_BASEINFO_DICT'
    Id = Column(String, primary_key=True)
    DictonaryId = Column('DICTIONARY_ID', Integer, ForeignKey(
        'DM_BASEINFO_CONFIG.DICTIONARY_ID'))
    DictKey = Column('DICTIONARY_KEY', Integer)
    DictValue = Column('DICTIONARY_VALUE', String)
    KeyOrValue = Column('KEY_OR_VALUE', Integer)
    SortNo = Column('SORT_NO', Integer)


class ClassifyTechparamConfig(Base):
    __tablename__ = 'DM_CLASSIFY_TECHPARAM'
    Id = Column(String, primary_key=True)
    ClassifyId = Column('CLASSIFY_ID', String, ForeignKey('DM_CLASSIFY.ID'))
    TechparamId = Column('TECHPARAM_ID', String)
    ColumnName = Column('COLUMN_NAME', String)
    TechparamInfo = relationship('TechparamConfig', uselist=False)
    TechparamType = Column('TECH_PARAM_TYPE', Integer)
    IsShow = Column('IS_SHOW', Integer)
    SortNo = Column('SORT_NO', Integer)


class TechparamConfig(Base):
    __tablename__ = 'DM_TECHPARAM'
    Id = Column(String, ForeignKey(
        'DM_CLASSIFY_TECHPARAM.TECHPARAM_ID'), primary_key=True)
    TechparamName = Column('TECHPARAM_NAME', String)
    DataType = Column('DATA_TYPE', Integer)
    DataLength = Column('DATA_LENGTH', Integer)


class ClassifyConfig(Base):
    __tablename__ = 'DM_CLASSIFY'
    Id = Column('ID', String, primary_key=True)
    ClassifyName = Column('CLASSIFY_NAME', String)
    FullName = Column('FULL_NAME', String)
    TableName = Column('TABLE_NAME', String)
    IsShow = Column('IS_SHOW', Integer)
    SortNo = Column('SORT_NO', Integer)
    BaseinfoTypeId = Column('BASEINFO_TYPEID', String)
    BaseinfoConfigs = relationship('BaseinfoConfig')
    TechparamConfigs = relationship('ClassifyTechparamConfig')


class BasicInfo(object):
    def __init__(self, baseinfoTypeid):
        self.BaseinfoTypeid = baseinfoTypeid
        self.Items = []


class TechparamInfo(object):
    def __init__(self, classifyId):
        self.ClassifyId = classifyId
        self.Items = []
