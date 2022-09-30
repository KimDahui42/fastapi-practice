from sqlalchemy import Column, Integer, String, Date
from app.database.connectPostgre import Base


class CrawledData(Base):
    __tablename__ = "crawled_datas" 
    id = Column(Integer, primary_key=True, index=True)   
    title = Column(String(length=200), default="정보없음")
    agency = Column(String(length=40), default="정보없음")
    contact = Column(String(length=200), default="정보없음")
    event_date = Column(String(length=30), default="정보없음")
    crawled_date = Column(Date)
    source = Column(String(length=200), default="정보없음")
