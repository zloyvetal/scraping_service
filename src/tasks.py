from sqlalchemy import select

from scraper import scrape
from models import GameInfoModel
from root import scheduler, settings, Session


@scheduler.scheduled_job('interval', minutes=settings.SCRAP_INTERVAL_MINUTES)
async def scrap() -> None:
    scrape_data = scrape(settings.SCRAP_TARGET_URL)

    with Session() as session, session.begin():
        exist = session.execute(select(GameInfoModel.name)).scalars().all()

        for data in scrape_data:
            if data.name in exist:
                continue

            gi = GameInfoModel.from_data(data)
            exist.append(gi.name)

            session.add(gi)
