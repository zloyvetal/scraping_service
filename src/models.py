from sqlalchemy import Column, String, BigInteger, ARRAY

from root import BaseModel
from schemas import GameInfoSchema


class GameInfoModel(BaseModel):
    __tablename__ = "games_2023"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, unique=True)
    publisher = Column(String)
    scheduled = Column(String)
    platforms = Column(ARRAY(String))
    genre = Column(String)
    description = Column(String)
    source_url = Column(String)
    info_url = Column(String)
    distribution_channels = Column(ARRAY(String))

    def __int__(self, game, publisher, developer, scheduled, platforms, genres, description, source_url,
                distribution_channel, info_url):
        self.name = game
        self.publisher = publisher.value
        self.developer = developer
        self.scheduled = scheduled
        self.platforms = platforms
        self.genre = genres
        self.description = description
        self.info_url = info_url
        self.source_url = source_url
        self.distribution_channels = distribution_channel

    def __repr__(self):
        return f"The {self.name} will be published byt {self.publisher} at {self.scheduled_at}"

    @classmethod
    def from_data(cls, gi: GameInfoSchema) -> 'GameInfoModel':
        return cls(
            name=gi.name,
            publisher=gi.publisher.value,
            scheduled=gi.scheduled,
            platforms=gi.platforms,
            genre=gi.genre,
            description=gi.description,
            info_url=gi.info_url,
            source_url=gi.source_url,
            distribution_channels=gi.distribution_channels,
        )
