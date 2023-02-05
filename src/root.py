from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from pydantic import BaseSettings, PostgresDsn, AnyHttpUrl
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


class Settings(BaseSettings):
    DEBUG: bool = False
    PG_DSN: PostgresDsn

    SCRAP_INTERVAL_MINUTES: int = 24 * 60
    SCRAP_TARGET_URL: AnyHttpUrl = "https://www.gamepressure.com/games/games_release_dates.asp?CZA=6"


settings = Settings(_env_file=".env")

engine = create_engine(settings.PG_DSN, echo=settings.DEBUG)
Session = sessionmaker(bind=engine)
BaseModel = declarative_base()

app = FastAPI(debug=settings.DEBUG)

scheduler = AsyncIOScheduler()


@app.on_event("startup")
async def startup() -> None:
    scheduler.start()


@app.on_event("shutdown")
async def shutdown() -> None:
    scheduler.shutdown()
