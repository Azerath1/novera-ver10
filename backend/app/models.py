from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Title(Base):
    __tablename__ = "titles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    author = Column(String)
    cover_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    chapters = relationship("Chapter", back_populates="title_rel")

class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    title_id = Column(Integer, ForeignKey("titles.id"))
    number = Column(Integer)
    name = Column(String)
    content = Column(Text)

    title_rel = relationship("Title", back_populates="chapters")