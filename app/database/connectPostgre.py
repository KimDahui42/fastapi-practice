from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.common.config import get_secret


engine = create_engine(
    "postgresql://{username}:{password}@{host}:{port}/{db_name}".format(
        username=get_secret("POSTGRES_USERNAME"),
        password=get_secret("POSTGRES_PASSWORD"),
        host="127.0.0.1",
        port="5432",
        db_name="ExampleDB",
    )
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
