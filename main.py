from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, CHAR, Integer, create_engine, Column, BINARY
from sqlalchemy.orm import DeclarativeBase, sessionmaker, declarative_base
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from scraper import scraper

Base = declarative_base()


class GameInfo(Base):
    __tablename__ = "games_2023"

    game_name = Column(
        'Game name',
        String,
        primary_key=True,
        unique=True
    )

    publisher = Column(
        'Publisher',
        String
    )

    developer = Column(
        'Developer',
        String
    )

    scheduled = Column(
        'Release date',
        String
    )

    platforms = Column(
        'Platforms',
        String
    )

    genres = Column(
        'Genres',
        String
    )

    game_description = Column(
        'Game description',
        String
    )

    source = Column(
        'Link to the source',
        String
    )

    game_info_link = Column(
        "Link to trailer or screenshots for the game",
        String
    )

    distribution_channels = Column(
        'Distribution channels',
        String
    )

    def __int__(self, game, publisher, developer, scheduled, platforms, genres, description, source,
                distribution_channel, game_info_link):
        self.game_name = game
        self.publisher = publisher
        self.developer = developer
        self.scheduled = scheduled
        self.platforms = platforms
        self.genres = genres
        self.description = description
        self.game_info_link = game_info_link
        self.source = source
        self.distribution_channels = distribution_channel

    def __repr__(self):
        return f"The {self.game_name} will be published byt {self.publisher} at {self.scheduled}"


engine = create_engine("postgresql://postgres:123@localhost/games_db")
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
url = 'https://www.gamepressure.com/games/games_release_dates.asp?CZA=6'
scrape_data = scraper(url)
for row in scrape_data:
    if not session.query(GameInfo).filter_by(game_name=row['game_name']).first():
        session.add(GameInfo(
            game_name=row['game_name'],
            publisher=row['publisher'],
            developer=row['developer'],
            scheduled=row['date'],
            platforms=row['platforms'],
            genres=row['genre'],
            description=row['game_description'],
            game_info_link=row['img_link'],
            source=row['source'],
            distribution_channels=row['distribution_channels'],
        ))

session.commit()
