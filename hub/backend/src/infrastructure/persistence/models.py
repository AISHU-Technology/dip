"""ORM 模型定义 (SQLAlchemy)"""
from datetime import datetime
from sqlalchemy import (
    Column,
    BigInteger,
    String,
    Text,
    DateTime,
    SmallInteger,
    Index,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class AppModel(Base):
    """应用表模型"""
    __tablename__ = "app"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="ID")
    name = Column(String(128), nullable=False, comment="应用名称")
    description = Column(String(800), nullable=True, comment="应用描述")
    cover_base64 = Column(Text, nullable=True, comment="封面Base64")
    creator_id = Column(String(36), nullable=False, comment="创建者ID")
    create_time = Column(DateTime(3), nullable=False, default=datetime.now, comment="创建时间")
    editor_id = Column(String(36), nullable=False, comment="编辑者ID")
    edit_time = Column(
        DateTime(3),
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
        comment="编辑时间"
    )
    dev_mode = Column(SmallInteger, nullable=False, comment="开发模式：1=上传,2=在线开发")
    publish_status = Column(SmallInteger, nullable=False, comment="发布状态：0=未发布,1=已发布,2=未发布更新")
    release_app_package_id = Column(BigInteger, nullable=False, default=0, comment="发布的包ID")
    is_deleted = Column(SmallInteger, default=0, comment="是否删除")
    
    # 关联关系
    packages = relationship("AppPackageModel", back_populates="app", lazy="selectin")
    
    __table_args__ = (
        Index("idx_publish_status", "publish_status"),
        Index("idx_edit_time", "edit_time"),
    )


class AppPackageModel(Base):
    """应用包表模型"""
    __tablename__ = "app_package"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="ID")
    app_id = Column(BigInteger, ForeignKey("app.id"), nullable=False, comment="应用ID")
    name = Column(String(128), nullable=False, comment="包名称")
    proton_chart_code = Column(String(512), nullable=False, comment="Proton chart ID")
    proton_image_code = Column(String(512), nullable=False, comment="Proton image ID")
    upload_user_id = Column(String(36), nullable=False, comment="上传者ID")
    upload_time = Column(
        DateTime(3),
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now,
        comment="上传时间"
    )
    
    # 关联关系
    app = relationship("AppModel", back_populates="packages")
    
    __table_args__ = (
        Index("idx_app_id", "app_id"),
        Index("idx_upload_time", "upload_time"),
    )

