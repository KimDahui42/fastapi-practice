from sqlalchemy import Column, Integer, String, Date
from app.database.connectPostgre import Base


class CrawledData(Base):
    __tablename__ = "crawled_datas"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="정보없음")
    agency = Column(String, default="정보없음")
    contact = Column(String, default="정보없음")
    event_date = Column(String, default="정보없음")
    crawled_date = Column(Date)
    source = Column(String, default="정보없음")
