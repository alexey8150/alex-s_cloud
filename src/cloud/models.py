from datetime import datetime

from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP


class File(Base):
    __tablename__ = 'userfiles'

    id = Column(Integer, primary_key=True)
    filename = Column(String(100), nullable=False)
    user_id = Column('user_id', Integer, ForeignKey('user.id'))
    upload_at = Column('upload_at', TIMESTAMP, default=datetime.utcnow)
