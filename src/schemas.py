from enum import Enum

from pydantic import AnyHttpUrl, BaseModel

from root import settings


class HealthSchema(BaseModel):
    DEBUG: bool = settings.DEBUG
    SCRAP_INTERVAL_MINUTES: int = settings.SCRAP_INTERVAL_MINUTES
    SCRAP_TARGET_URL: AnyHttpUrl = settings.SCRAP_TARGET_URL


class GameInfoListItemSchema(BaseModel):
    id: int
    name: str


class GameInfoListSchema(BaseModel):
    items: list[GameInfoListItemSchema]


class GameInfoSchema(BaseModel):
    class Config:
        orm_mode = True

    class PublisherEnum(Enum):
        THO_KEY = "2K"
        REMEDY = "Remedy"
        UBISOFT = "Ubisoft"
        INFINITY_WARD = "Infinity Ward"
        ANNAPURNA_INTERACTIVE = "Annapurna Interactive"
        ELECTRONIC_ARTS = "Electronic Arts"
        ZYNGA = "Zynga"
        People_Can_Fly = "People Can Fly"
        SQUARE_ENIX = "Square Enix"
        ACTIVISION = "Activision"

    name: str
    publisher: PublisherEnum
    scheduled: str
    platforms: list[str]
    genre: str
    description: str
    info_url: AnyHttpUrl
    source_url: AnyHttpUrl
    distribution_channels: list[str]


