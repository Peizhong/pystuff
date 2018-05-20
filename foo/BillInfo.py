from foo.Base import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, PrimaryKeyConstraint, ForeignKeyConstraint
from sqlalchemy.orm import relationship


class WorkspaceVO(Base):
    __tablename__ = 'DM_WORKSPACE'
    Id = Column('ID', String, primary_key=True)
    BusinessBillId = Column('BUSINESS_BILL_ID', String)
    BusinessBillType = Column('BUSINESS_BILL_TYPE', Integer)
    ObjectId = Column('OBJECT_ID', String)
    WorkspaceName = Column('WORKSPACE_NAME', String)
    UpdateTime = Column('UPDATE_TIME', DateTime)


class MainTransferVO(Base):
    __tablename__ = 'DM_MAIN_TRANSFER'
    Id = Column('ID', String, primary_key=True)
    BusinessBillCode = Column('BUSINESS_BILL_CODE', String)
    Workspaces = relationship('WorkspaceVO', uselist=True)
    __table_args__ = (
        ForeignKeyConstraint(
            ['ID'],
            ['DM_WORKSPACE.BUSINESS_BILL_ID']
        ),
    )
