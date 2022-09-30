from dataclasses import dataclass
from fastapi import Request, FastAPI
from pathlib import Path
from app.database.connectPostgre import db
from app.database.models import CrawledData
from apscheduler.schedulers.background import BackgroundScheduler
from app.crawling.crawler import getData


BASE_DIR = Path(__file__).resolve().parent.parent
app = FastAPI()
db.init_app(app)
# Dependency


@app.get("/")
def root(request: Request):
    data = next(db.get_db())
    context = data.query(CrawledData).all()
    return {"context" : context}

@app.get("/crawl")
def crawlData():
    database = next(db.get_db())
    data = getData()
    for key in data:
        for item in data[key]:
            current = CrawledData(
                title=item["title"],
                agency=item["agency"],
                contact=item["contact"],
                event_date=item["event_date"],
                crawled_date=item["upload_date"],
                source=key
            )
            database.add(current)
            database.commit()
    return {"message":"saved"}
            
# 크롤링 관련
sched = BackgroundScheduler(timezone="Asia/Seoul")


# 매일 스케줄러 작동, 크롤러 실행\
@sched.scheduled_job("cron", hour="16", minute="41", id="crawl_data")
def job():
    database = next(db.get_db())
    data = getData()
    for key in data:
        for item in data[key]:
            current = CrawledData(
                title=item["title"],
                agency=item["agency"],
                contact=item["contact"],
                event_date=item["event_date"],
                crawled_date=item["upload_date"],
                source=key
            )
            database.add(current)
            database.commit()


@app.on_event("startup")
def startup_crawler_scheduler():
    sched.start()


@app.on_event("shutdown")
def close_crawler_scheduler():
    sched.shutdown()
