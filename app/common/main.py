from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app.database.connectPostgre import SessionLocal, Base, engine
from app.models.crawledData import CrawledData
from apscheduler.schedulers.background import BackgroundScheduler


app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {"message": "Hello World!"}


# 크롤링 관련
sched = BackgroundScheduler(timezone="Asia/Seoul")


@app.on_event("startup")
def on_app_start():
    """
    before app starts
    """
    Base.metadata.create_all(bind=engine)


'''@app.on_event("shutdown")
async def on_app_shutdown():
    """
    after app shutdown
    """
    await mongodb.close()'''


# 매일 스케줄러 작동, 크롤러 실행\
@sched.scheduled_job("cron", hour="1", minute="30", id="remove_inactive_image")
def job():
    db = next(get_db())
    inactive_image_list = db.query(Image).filter(Image.state == "INACTIVE").all()
    for image in inactive_image_list:
        db.delete(image)


def start_image_scheduler():
    sched.start()
