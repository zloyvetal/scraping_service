from models import *
from root import engine, BaseModel


def main() -> None:
    BaseModel.metadata.drop_all(bind=engine)
    BaseModel.metadata.create_all(bind=engine)


if __name__ == "__main__":
    main()
