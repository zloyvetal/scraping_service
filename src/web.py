from fastapi import HTTPException, APIRouter
from sqlalchemy import select

from models import GameInfoModel
from root import Session
from schemas import HealthSchema, GameInfoListSchema, GameInfoSchema

tech = APIRouter(prefix="/-")
api = APIRouter(prefix="/api")


@tech.get("/health", response_model=HealthSchema)
def health():
    return HealthSchema()


@api.get("/games", response_model=GameInfoListSchema)
def game_list():
    with Session() as sessions:
        stmt = select(GameInfoModel.id, GameInfoModel.name)
        res = sessions.execute(stmt).all()

    items = [{"id": i[0], "name": i[1]} for i in res]
    return GameInfoListSchema.parse_obj({"items": items})


@api.get("/games/{key:int}", response_model=GameInfoSchema, responses={404: {"description": "Not found"}})
def game_details(key: int):
    with Session() as session:
        stmt = select(GameInfoModel).where(GameInfoModel.id == key)
        res = session.execute(stmt).scalars().one_or_none()

    if res is None:
        raise HTTPException(status_code=404, detail="Game info does not exist")

    return GameInfoSchema.from_orm(res)
